import io
import json
from PIL.Image import Image
from api.grpc.vector_processor import vector_processor_pb2
from core import models


def save_image(image: Image):
    with io.BytesIO() as bio:
        image.save(bio, 'png')
        bio.seek(0)
        return bio.read()


def map_userupdate(userupdate: models.UserUpdate):
    return vector_processor_pb2.UserInfo(
        first_name=userupdate.first_name,
        second_name=userupdate.second_name,
        avatar=save_image(userupdate.avatar),
        country=userupdate.country,
        city=userupdate.city,
        birthday=userupdate.birthday,
    )


def map_itemupdate(itemupdate: models.ItemUpdate):
    photos = [save_image(p.img) for p in itemupdate.photos]

    return vector_processor_pb2.ItemInfo(
        name=itemupdate.name,
        price=itemupdate.price,
        description=itemupdate.description,
        attributes_json=json.dumps(itemupdate.attributes, separators=(',', ':')),
        photos=photos
    )


def map_vectorizeduser(vectorized_user: models.VectorizedUser):
    return vector_processor_pb2.Embedding(
        data=[x for x in vectorized_user.embedding.data]
    )


def map_feedback(feedback: models.ItemFeedback):
    feedback_pb2: vector_processor_pb2.AdjustUserRequest.FeedbackType

    if feedback.feedback == models.FeedbackType.POSITIVE:
        feedback_pb2 = vector_processor_pb2.AdjustUserRequest.FeedbackType.POSITIVE
    else:
        feedback_pb2 = vector_processor_pb2.AdjustUserRequest.FeedbackType.NEGATIVE

    return vector_processor_pb2.AdjustUserRequest.Feedback(
        item=vector_processor_pb2.Embedding(
            data=[x for x in feedback.item.embedding.data]
        ),
        feedback=feedback_pb2
    )


def map_feedback_list(feedbacks: list[models.ItemFeedback]):
    return list(map(map_feedback, feedbacks))


def reverse_map_embedding(embedding: vector_processor_pb2.Embedding):
    return models.Embedding(data=[x for x in embedding.data])
