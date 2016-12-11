import json
import logging
from pathlib import Path
from time import sleep
from typing import List

from vkdump.api import get_api
from vkdump.entities.posts import get_post_id
from vkdump.models.attaches_loader import AttachesLoader


class FeedLoader:
    def __init__(self, feed_path : Path):
        self.feed_path = feed_path
        self.api = get_api()
        self.attaches_loader = AttachesLoader()
        self.logger = logging.getLogger(FeedLoader.__name__)

    def _query_new(self, offset: int) -> List[dict]:
        raise NotImplementedError

    def load_feed(self) -> List[dict]:
        with self.feed_path.open('r') as fo:
            favs = json.load(fo)
            return favs

    def _save_feed(self, favs: List[dict]) -> None:
        with self.feed_path.open('w') as fo:
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
            self.logger.info("Loaded %d new posts", len(result))
            new_posts.extend(result)
            if not old_ids.isdisjoint(result_ids) or len(result_ids) == 0:
                break
            sleep(0.5)  # TODO meh
        return new_posts
