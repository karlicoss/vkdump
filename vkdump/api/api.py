import logging
from typing import List, Dict

import vk

from vkdump.config import config

_COMMON_USER_FIELDS = "photo_id, verified, sex, bdate, city, country, home_town, " \
                      "has_photo, photo_50, photo_100, photo_200_orig, photo_200, " \
                      "photo_400_orig, photo_max, photo_max_orig, online, lists, " \
                      "domain, has_mobile, contacts, site, education, universities, " \
                      "schools, status, last_seen, followers_count, common_count, " \
                      "occupation, nickname, relatives, relation, personal, connections, " \
                      "exports, wall_comments, activities, interests, music, movies, " \
                      "tv, books, games, about, quotes, can_post, can_see_all_posts, " \
                      "can_see_audio, can_write_private_message, can_send_friend_request, " \
                      "is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, " \
                      "crop_photo, is_friend, friend_status, career, military, blacklisted, " \
                      "blacklisted_by_me".split(", ")

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

    def get_friends(self, user_id: str) -> List[Dict]:
        response = self.api.friends.get(
            user_id=user_id,
            fields=_COMMON_USER_FIELDS,
        )
        return response['items']

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
