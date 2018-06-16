import logging
from requests.exceptions import ConnectionError
from typing import List, Dict

import vk # type: ignore
from vk.exceptions import VkAPIError # type: ignore

from vkdump.config import config

import backoff # type: ignore

from kython.network import backoff_network_errors

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

# TODO ugh, still need some sort of common backof function

def is_deleted(e):
    return isinstance(e, VkAPIError) and e.code == 18

def is_tmp_network_error(e):
    if isinstance(e, (ConnectionError, ConnectionRefusedError)):
        return True
    return False

# actually, that could be extracted in kython
def fatal_exception(e):
    if is_deleted(e):
        # no point trying again
        return True
    else:
        return not is_tmp_network_error(e)

def on_backoff(args=None, **kwargs):
    self = args[0]
    self.logger.info("Backing off")
    # TODO something more meaningful?

def on_giveup(args=None, **kwargs):
    self = args[0]
    self.logger.warning("Giving up!")

def hdlr(delegate):
    def fun(details):
        return delegate(**details)
    return fun

# TODO: limits
class VkApi:
    def __init__(self) -> None:
        session = vk.Session(access_token=config.ACCESS_TOKEN)
        self.api = vk.API(session=session, v='5.53')  # TODO: inject
        self.logger = logging.getLogger('VkApi')
        import coloredlogs # type: ignore
        coloredlogs.install(logger=self.logger)
        self.logger.setLevel(logging.INFO)

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=2,
        giveup=fatal_exception,
        on_backoff=hdlr(on_backoff),
        on_giveup=hdlr(on_giveup),
    )
    def _with_backoff(self, method, *args, **kwargs):
        return method(*args, **kwargs)

    def get_friends(self, user_id: str) -> List[Dict]:
        response = backoff_network_errors(
            self.api.friends.get,
            self.logger,
            user_id=user_id,
            fields=_COMMON_USER_FIELDS,
        )
        return response['items']

    def get_several(self, user_ids: List[str]):
        return backoff_network_errors(
            self.api.users.get,
            self.logger,
            user_ids=user_ids,
            fields=_COMMON_USER_FIELDS,
        )

    def get_single(self, user_id: str):
        return self.get_several(user_ids=[user_id])[0]

    def get_subscriptions(self, user_id: str):
        return backoff_network_errors(
            self.api.users.getSubscriptions,
            self.logger,
            user_id=user_id,
        )

    def get_favs(self, offset: int, count: int = 100) -> List[dict]:
        response = backoff_network_errors(
            self.api.fave.getPosts,
            self.logger,
            offset=offset,
            count=count,
        )
        return response['items']

    def get_wall(self, owner_id: str, offset: int, count: int = 100) -> List[dict]:
        response = self._with_backoff(
            self.api.wall.get,
            owner_id=owner_id,
            offset=offset,
            count=count,
        )
        return response['items']

    def get_posts_by_ids(self, ids: List[str]) -> List[dict]:
        ids_string = ','.join(ids)
        response = backoff_network_errors(
            self.api.wall.getById,
            self.logger,
            posts=ids_string,
            extended=1
        )
        return response['items']



def get_api() -> VkApi:
    return VkApi()
