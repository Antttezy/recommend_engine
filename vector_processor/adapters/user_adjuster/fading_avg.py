import math

import numpy as np
from core import models
from vector_processor.core import ports


class FadingAvgUserAdjuster(ports.UserAdjuster):
    def __init__(self, like_learning_rate: float, dislike_learning_rate: float, decay: float):
        super().__init__()
        self.like_learning_rate = like_learning_rate
        self.dislike_learning_rate = dislike_learning_rate
        self.decay = decay

    def adjust_user_embedding(self, user, feedbacks):
        user_emb = np.array(user.embedding.data, dtype=np.float32)

        for i, feedback in enumerate(feedbacks):
            item_emb = np.array(feedback.item.embedding.data, dtype=np.float32)
            weight = math.exp(-self.decay * i)
            delta = weight * item_emb

            if feedback.feedback == models.FeedbackType.POSITIVE:
                user_emb += delta * self.like_learning_rate
            else:
                user_emb -= delta * self.dislike_learning_rate

        norm = np.linalg.norm(user_emb)
        if norm > 1e-9:
            user_emb = user_emb / norm

        return models.Embedding(data=user_emb.tolist())
