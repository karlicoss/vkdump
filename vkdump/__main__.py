#!/usr/bin/env python3
import logging

from vkdump.models.favs_loader import FavsLoader
from vkdump.models.feed_loader import FeedLoader
from vkdump.models.wall_loader import WallLoader


def update_feed(loader: FeedLoader):
    logging.basicConfig(level=logging.INFO)
    logging.info("Current loader: %s", loader.__class__.__name__)
    before = loader.load_feed()
    logging.info("Before: %d posts", len(before))
    loader.update()
    after = loader.load_feed()
    logging.info("After: %d posts", len(after))


def main():
    update_feed(FavsLoader())
    update_feed(WallLoader())


if __name__ == '__main__':
    main()
