import json
import logging
import os
from pathlib import Path
from time import sleep
from typing import List

from atomicwrites import atomic_write

from vkdump.api import get_api
from vkdump.api.api import QUERY_SLEEP_TIME
from vkdump.entities.posts import get_post_id
from vkdump.models.attaches_loader import AttachesLoader


class FeedLoader:
    def __init__(self, feed_dir: Path, logger_tag: str='FeedLoader') -> None:
        self.feed_dir = feed_dir
        if not feed_dir.exists():
            os.makedirs(feed_dir.as_posix())
        self.feed_file = feed_dir.joinpath('feed.json')
        self.api = get_api()
        self.attaches_loader = AttachesLoader(self.feed_dir.joinpath('images'))
        self.logger = logging.getLogger(logger_tag)

    def _query_new(self, offset: int) -> List[dict]:
        raise NotImplementedError

    def load_feed(self) -> List[dict]:
        if not self.feed_file.exists():
            self.logger.warn("File %s does not exist! Assuming empty timeline", self.feed_file.as_posix())
            return []

        with self.feed_file.open('r') as fo:
            favs = json.load(fo)
            return favs

    def _save_feed(self, favs: List[dict]) -> None:
        with atomic_write(self.feed_file.as_posix(), overwrite=True) as fo:
            json.dump(favs, fo, indent=5, ensure_ascii=False, sort_keys=True)

    def update(self):
        old_favs = self.load_feed()
        new_favs = self._get_new_posts(old_favs)
        # TODO download some old
        self.attaches_loader.download_attaches(new_favs)
        result = new_favs
        result.extend(old_favs)
        self._save_feed(result)

    def _get_new_posts(self, old_posts: List[dict]) -> List[dict]:
        old_ids = {get_post_id(p) for p in old_posts}

        # TODO use map to ensure uniqueness?
        new_posts = []  # type: List[dict]

        while True:
            result = self._query_new(len(new_posts))
            result_ids = {get_post_id(p) for p in result}
            result = [p for p in result if get_post_id(p) not in old_ids]
            self.logger.debug("Loaded %d new posts", len(result))
            new_posts.extend(result)
            if not old_ids.isdisjoint(result_ids) or len(result_ids) == 0:
                break
            sleep(QUERY_SLEEP_TIME)
        return new_posts
