from uuid import UUID


ITEMS_LIST_KEY = 'user/{id}/feed'


def get_items_list_key(user_id: UUID):
    return ITEMS_LIST_KEY.format(id=user_id)
