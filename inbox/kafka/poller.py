import asyncio
import datetime
import logging
from typing import Optional

from confluent_kafka.aio import AIOConsumer
from confluent_kafka import Message

from core.errors import BaseError
from inbox.core.ports import UpdateHandler
from . import const
from inbox.kafka.retry import MessageRetry


logger = logging.getLogger(__name__)


class KafkaPoller:
    def __init__(self,
                 endpoint: str,
                 handlers: dict[str, UpdateHandler],
                 retry: Optional[MessageRetry]):
        config = {
            'bootstrap.servers': endpoint,
            'group.id': const.TOPIC_GROUP,
            "auto.offset.reset": "earliest",
            "enable.auto.offset.store": False,
            "enable.auto.commit": False
        }

        topics = [x for x in handlers.keys()]

        self.__config = config
        self.__handlers = handlers
        self.__retry = retry
        self.__topics = topics
        self.__poll_tasks = []
        self.__shutdown_event = asyncio.Event()
        self.__start_event = asyncio.Event()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.shutdown()

    async def start(self):
        if self.__start_event.is_set():
            return

        self.__start_event.set()

        for topic in self.__topics:
            task = asyncio.create_task(self.__poll_loop(topic))
            self.__poll_tasks.append(task)

    async def shutdown(self):
        if self.__shutdown_event.is_set() or not self.__start_event.is_set():
            return

        self.__shutdown_event.set()
        await asyncio.gather(*self.__poll_tasks, return_exceptions=True)

    async def __poll_loop(self, topic: str):
        async with AIOConsumer(self.__config) as consumer:
            await consumer.subscribe([topic])
            logger.info("Started consumer for topic %s", topic)

            while not self.__shutdown_event.is_set():
                msg: Message | None = await consumer.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    continue

                topic = msg.topic()
                logger.info("Got message from topic %s", topic)

                if topic is None:
                    continue

                await self.__msg_sleep(msg)

                if self.__shutdown_event.is_set():
                    break

                try:
                    handler = self.__handlers.get(topic, None)
                    logger.debug("Message handler is %s", handler)

                    if handler is None:
                        continue

                    await handler.handle(msg.value())

                except BaseError as e:
                    err = ": ".join([*e.args])
                    logger.error("Could not handle message: %s", err)
                    await consumer.commit(message=msg, asynchronous=False)
                    logger.info("Message committed")
                except Exception as e:
                    logger.error("Encountered transient error", exc_info=True, stack_info=True)
                    retry = self.__retry
                    logger.debug("Retry handler is %s", retry)

                    try:
                        if retry is not None:
                            logger.info("Sending to retry queue...")
                            await retry.retry_message(msg)
                    except Exception as e:
                        logger.error("Could not retry", exc_info=True, stack_info=True)
                    else:
                        await consumer.commit(message=msg, asynchronous=False)
                        logger.info("Message committed")
                else:
                    await consumer.commit(message=msg, asynchronous=False)
                    logger.info("Message committed")

    async def __msg_sleep(self, msg: Message):
        headers = dict(msg.headers() or [])
        retry_at = headers.get("retry-at", None)
        retry_at = self.__decode_retry_at(retry_at)
        logger.debug("Parsed header retry-at %s", retry_at.isoformat() if retry_at else None)

        if retry_at is not None:
            diff = self.__seconds_diff(datetime.datetime.now(), retry_at)

            if diff > 0:
                logger.debug("Sleeping for %s seconds", diff)
                tasks = [
                    asyncio.create_task(asyncio.sleep(diff)),
                    asyncio.create_task(self.__shutdown_event.wait())
                ]

                await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    @staticmethod
    def __decode_retry_at(value: str | bytes | None) -> datetime.datetime | None:
        if value is None:
            return

        if isinstance(value, bytes):
            try:
                value = value.decode()
            except UnicodeDecodeError:
                return

        try:
            value = int(value)
        except ValueError:
            return

        return datetime.datetime.fromtimestamp(value)

    @staticmethod
    def __seconds_diff(a: datetime.datetime, b: datetime.datetime) -> float:
        delta = b - a
        return delta.total_seconds()
