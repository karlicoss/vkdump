#!/usr/bin/env python3.6
import logging

logger = logging.getLogger('vkdump')

import coloredlogs # type: ignore
from vk.exceptions import VkAPIError # type: ignore

from vkdump.api.api import VkApi, is_deleted
from vkdump.config import config
from vkdump.models.favs_loader import FavsLoader
from vkdump.models.feed_loader import FeedLoader
from vkdump.models.profiles_loader import ProfilesLoader
from vkdump.models.wall_loader import WallLoader


def update_feed(loader: FeedLoader):
    before = loader.load_feed()
    logger.info(f"Before: {len(before)} posts")
    loader.update()
    after = loader.load_feed()
    logger.info(f"After: {len(after)} posts")


def update_favs():
    logger.info("Updating favorites")
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
    logger.info(f"Walls updater: {len(ids)} IDs to update")
    for i, uid in enumerate(ids):
        logger.info(f"[{i}/{len(ids)}]: updating {uid}")
        update_feed(WallLoader(uid))


def update_profiles():
    ids = get_tracked_ids()
    logger.info("Profiles updater: %d IDs to update", len(ids))
    loader = ProfilesLoader()
    loader.update_all(ids)


def main():
    update_favs()
    update_profiles()
    update_all_walls()


if __name__ == '__main__':
    # TODO basicConfig might be useful to see whcih loggers are available
    # after that, turn them off?
    # or turn off individually?
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.getLogger('backoff').setLevel(logging.CRITICAL)
    coloredlogs.install(logger=logger)
    main()
