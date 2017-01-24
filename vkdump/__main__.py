#!/usr/bin/env python3
import logging

import coloredlogs
from vk.exceptions import VkAPIError

from vkdump.api.api import VkApi
from vkdump.config import config
from vkdump.models.favs_loader import FavsLoader
from vkdump.models.feed_loader import FeedLoader
from vkdump.models.profiles_loader import ProfilesLoader
from vkdump.models.wall_loader import WallLoader


def update_feed(loader: FeedLoader):
    before = loader.load_feed()
    logging.info("Before: %d posts", len(before))
    loader.update()
    after = loader.load_feed()
    logging.info("After: %d posts", len(after))


def update_favs():
    logging.info("Updating favorites")
    update_feed(FavsLoader())


def get_tracked_ids():
    ids = set()
    for i in config.IDS_TO_DUMP:
        if i == 'friends':
            api = VkApi()
            friends_ids = [str(f['id']) for f in api.get_friends(config.USER_ID)]
            ids.update(friends_ids)
        elif str.isnumeric(i):
            ids.add(i)
        else:
            raise AttributeError("Unexpected id " + i)
    ids = sorted(ids)  # for determinism
    return ids


def update_all_walls():
    ids = get_tracked_ids()
    logging.info("Walls updater: %d IDs to update", len(ids))
    for i, uid in enumerate(ids):
        logging.info("[%d/%d]: updating %s", i, len(ids), uid)
        try:
            update_feed(WallLoader(uid))
        except VkAPIError as e:
            if e.code == 18:
                logging.warning(str(e))
            else:
                raise e


def update_profiles():
    ids = get_tracked_ids()
    logging.info("Profiles updater: %d IDs to update", len(ids))
    loader = ProfilesLoader()
    loader.update_all(ids)


def main():
    update_favs()
    update_profiles()
    update_all_walls()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    coloredlogs.install(fmt="%(asctime)s [%(name)s] %(levelname)s %(message)s")
    main()
