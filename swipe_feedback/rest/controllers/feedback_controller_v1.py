from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core import models, ports, errors

from swipe_feedback.core.ports import SwipeBatchClient
from swipe_feedback.rest import dependencies as deps
from swipe_feedback.usecase import FeedbackUsecase, BatchSize


router = APIRouter(tags=['feedback'])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def handle_feedback(
    item_id: UUID = Query(alias='itemId'),
    feedback: Literal['positive', 'negative'] = Query(),
    user_id: UUID = Depends(deps.authenticated_user_id),
    item_repo: ports.VectorizedItemRepo = Depends(deps.item_repo),
    user_repo: ports.VectorizedItemRepo = Depends(deps.user_repo),
    vc: ports.VectorProcessorClient = Depends(deps.vector_processor_client),
    swipe_batch_client: SwipeBatchClient = Depends(deps.swipe_batch_client),
    feedback_batch: dict[str, int] = Depends(deps.feedback_batch),
):
    try:
        batch = BatchSize(feedback_batch['zero'], feedback_batch['default'])
        usecase = FeedbackUsecase(user_repo, item_repo, swipe_batch_client, vc, batch)
        fback = models.FeedbackType.POSITIVE if feedback == 'positive' \
            else models.FeedbackType.NEGATIVE

        await usecase.apply_feedback(user_id, item_id, fback)
    except errors.NotFoundError as e:
        errmsg = ': '.join(e.args)
        if errmsg.find('user') != -1:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'user not found')
        elif errmsg.find('item') != -1:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'item not found')
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
