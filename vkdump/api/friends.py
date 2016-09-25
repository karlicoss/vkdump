from api import get_api, VK_API_VERSION
from api.users import COMMON_USER_FIELDS


def get_friends(user_id: str):
    return get_api().friends.get(
            user_id=user_id,
            fields=COMMON_USER_FIELDS,
            v=VK_API_VERSION
    )
