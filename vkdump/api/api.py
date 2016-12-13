import logging
from typing import List

import vk

from vkdump.config import config

_COMMON_USER_FIELDS = [
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

# VK Api documentation claims you should not do more than three queries per second. This should be safe
QUERY_SLEEP_TIME = 1  # seconds


# TODO: limits
class VkApi:
    def __init__(self) -> None:
        session = vk.Session(access_token=config.ACCESS_TOKEN)
        # session = vk.Session()
        self.api = vk.API(session=session, v='5.53')  # TODO: inject
        self.logger = logging.getLogger('VkApi')
        self.logger.setLevel(logging.INFO)

    def get_friends(self, user_id: str):
        return self.api.friends.get(
            user_id=user_id,
            fields=_COMMON_USER_FIELDS,
        )

    def get_several(self, user_ids: List[str]):
        return self.api.users.get(
            user_ids=user_ids,
            fields=_COMMON_USER_FIELDS,
        )

    def get_single(self, user_id: str):
        return self.get_several(user_ids=[user_id])[0]

    def get_subscriptions(self, user_id: str):
        return self.api.users.getSubscriptions(
            user_id=user_id,
        )

    def get_favs(self, offset: int, count: int = 100) -> List[dict]:
        response = self.api.fave.getPosts(
            offset=offset,
            count=count,
        )
        return response['items']

    def get_wall(self, owner_id: str, offset: int, count: int = 100) -> List[dict]:
        response = self.api.wall.get(
            owner_id=owner_id,
            offset=offset,
            count=count,
        )
        return response['items']

    def get_posts_by_ids(self, ids: List[str]) -> List[dict]:
        ids_string = ','.join(ids)
        response = self.api.wall.getById(
            posts=ids_string,
            extended=1
        )
        return response['items']


def get_api() -> VkApi:
    return VkApi()
