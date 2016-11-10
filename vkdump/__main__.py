#!/usr/bin/env python3
import logging

from vkdump.models.favs_loader import FavsLoader


def update_favs():
    logging.basicConfig(level=logging.INFO)
    loader = FavsLoader()
    before = loader.load_favs()
    logging.info("Before: %d posts", len(before))
    loader.update()
    after = loader.load_favs()
    logging.info("After: %d posts", len(after))


def main():
    update_favs()


if __name__ == '__main__':
    main()
