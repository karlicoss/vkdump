import logging
from time import sleep
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

    # deprecated
    def get_all_favs(self) -> List[dict]:
        # TODO use map to ensure uniqueness?
        res = []  # type: List[dict]
        while True:
            new_favs = self.get_favs(offset=len(res))
            if len(new_favs) == 0:
                break

            print("Len: " + str(len(res)))
            self.logger.info("Got %d new favs", len(new_favs))
            sleep(0.5)  # TODO meh
            res.extend(new_favs)
        return res

    def get_posts_by_ids(self, ids: List[str]) -> List[dict]:
        ids_string = ','.join(ids)
        response = self.api.wall.getById(
            posts=ids_string,
            extended=1
        )
        return response['items']


def get_api() -> VkApi:
    return VkApi()
