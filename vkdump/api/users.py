from typing import List

from api import get_api, VK_API_VERSION

COMMON_USER_FIELDS = [
    'photo_id',
    'sex',
    'bdate',
    'city',
    'country',
    'home_town',
    'photo_max_orig',  # TODO
    'contacts',
    'education',
    'universities',
    'schools',
    'occupation',
    'relation',
    'personal',
    'connections',
    'activities',
    'interests',
    'music',
    'movies',
    'tv',
    'books',
    'games',
    'about',
    'quotes',
    'career',
    'military'
]


def get_several(user_ids: List[str]):
    return get_api().users.get(
            user_ids=user_ids,
            fields=COMMON_USER_FIELDS,
            v=VK_API_VERSION
    )


def get_single(user_id: str):
    return get_several(user_ids=[user_id])[0]


def get_subscriptions(user_id: str):
    return get_api().users.getSubscriptions(user_id=user_id)
