import asyncio
from dataclasses import dataclass
import datetime
import logging
from typing import Callable

from confluent_kafka import Message, Producer, KafkaException

from . import const


logger = logging.getLogger(__name__)


@dataclass
class RetryConfig:
    topic_name: str
    wait_seconds: int


class MessageRetry():
    def __init__(self,
                 endpoint: str,
                 retry_configs: dict[str, list[RetryConfig]],
                 topic_to_configname: Callable[[str], str]):
        config = {
            'bootstrap.servers': endpoint,
            'client.id': const.PROCUCER_ID,
            'enable.idempotence': True,
            'acks': 'all'
        }

        self.__producer = Producer(config)
        self.retry_configs = retry_configs
        self.__topic_to_configname = topic_to_configname
        self.__poller_task = None
        self.__shutdown_event = asyncio.Event()
        self.__start_event = asyncio.Event()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.shutdown()
        await asyncio.to_thread(self.__producer.flush)

    async def start(self):
        if self.__start_event.is_set():
            return

        self.__start_event.set()
        self.__poller_task = asyncio.create_task(self.__poll_loop())

    async def shutdown(self):
        if self.__shutdown_event.is_set() or not self.__start_event.is_set():
            return

        self.__shutdown_event.set()
        await asyncio.gather(self.__poller_task, return_exceptions=True)

    async def retry_message(self, msg: Message):
        retry_count = self.__msg_retry_count(msg)
        logger.debug("Message retry count: %s", retry_count)

        if retry_count < 0:
            logger.debug("Incorrect retry-count, clamping to 0")
            retry_count = 0

        topic = self.__topic_to_configname(msg.topic() or '')
        retry_config = self.retry_configs.get(topic or '', None)

        if retry_config is None:
            logger.debug("Retry config not found, message dropped")
            return  # DROP

        if retry_count >= len(retry_config):
            logger.debug("Retry count exceeded, message dropped")
            return  # DROP

        retry_config = retry_config[retry_count]
        logger.debug("Retry config is %s", retry_config.__repr__())
        retry_at = self.__get_retry_at_value(retry_config.wait_seconds)
        retry_count += 1
        self.__set_retry_headers(msg, retry_at, retry_count)

        logger.debug("Message retry headers retry-at=%s retry-count=%s", retry_at, retry_count)
        logger.debug("Sending message to topic %s", retry_config.topic_name)
        await self.__produce_async(msg, retry_config.topic_name)
        logger.debug("Successfully sent message")

    async def __produce_async(self, msg: Message, topic: str):
        loop = asyncio.get_running_loop()
        done = asyncio.Event()
        error = None

        def callback(err, kafka_msg):
            nonlocal error
            error = err
            loop.call_soon_threadsafe(done.set)

        self.__producer.produce(
            topic=topic,
            key=msg.key(),
            value=msg.value(),
            headers=msg.headers(),
            on_delivery=callback,
        )

        await done.wait()

        if error is not None:
            raise KafkaException(error)

    async def __poll_loop(self):
        while not self.__shutdown_event.is_set():
            self.__producer.poll(0)
            await asyncio.sleep(0.01)

    def __msg_retry_count(self, msg: Message):
        headers = dict(msg.headers() or [])
        retry_count = headers.get('retry-count', b'0')
        return int(retry_count)

    def __get_retry_at_value(self, timeout: int):
        now = datetime.datetime.now().timestamp()
        retry_at = round(now + timeout)
        return retry_at

    def __set_retry_headers(self, msg: Message, retry_at: int, retry_count: int):
        headers = dict(msg.headers() or [])
        headers['retry-count'] = str(retry_count)
        headers['retry-at'] = str(retry_at)
        msg.set_headers(headers)
