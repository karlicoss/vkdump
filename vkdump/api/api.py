from typing import List

import vk

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
    def __init__(self):
        self.api = vk.API(vk.Session())  # TODO: inject
        self.api_version = '5.53'

    def get_friends(self, user_id: str):
        return self.api.friends.get(
            user_id=user_id,
            fields=_COMMON_USER_FIELDS,
            v=self.api_version,
        )

    def get_several(self, user_ids: List[str]):
        return self.api.users.get(
            user_ids=user_ids,
            fields=_COMMON_USER_FIELDS,
            v=self.api_version,
        )

    def get_single(self, user_id: str):
        return self.get_several(user_ids=[user_id])[0]

    def get_subscriptions(self, user_id: str):
        return self.api.users.getSubscriptions(user_id=user_id)


def get_api() -> VkApi:
    return VkApi()
