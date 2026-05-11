from uuid import UUID

from pydantic import BaseModel, Field


class FeedItemResponse(BaseModel):
    id: UUID = Field()


feed_show_item_responses = {
    200: {
        'model': FeedItemResponse
    },
    401: {
        'description': 'Missing or invalid Authorization header'
    }
}

feed_next_item_responses = feed_show_item_responses
