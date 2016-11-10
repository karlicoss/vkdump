import json
import logging
from pathlib import Path
from time import sleep
from typing import List

from vkdump.api import get_api
from vkdump.config import config
from vkdump.entities.posts import get_post_id
from vkdump.models.attaches_loader import AttachesLoader


class FavsLoader:
    def __init__(self):
        self.favs_path = config.FAVS  # type: Path
        self.api = get_api()
        self.attaches_loader = AttachesLoader()
        self.logger = logging.getLogger(FavsLoader.__name__)

    def load_favs(self) -> List[dict]:
        with self.favs_path.open('r') as fo:
            favs = json.load(fo)
            return favs

    def _save_favs(self, favs: List[dict]) -> None:
        with self.favs_path.open('w') as fo:
            json.dump(favs, fo, indent=5, ensure_ascii=False, sort_keys=True)

    def update(self):
        old_favs = self.load_favs()
        new_favs = self._get_new_posts(old_favs)
        # TODO download some old
        self.attaches_loader.download_attaches(new_favs)
        result = new_favs
        result.extend(old_favs)
        self._save_favs(result)

    def _get_new_posts(self, old_favs: List[dict]) -> List[dict]:
        old_ids = {get_post_id(p) for p in old_favs}

        # TODO use map to ensure uniqueness?
        new_favs = []  # type: List[dict]

        while True:
            result = self.api.get_favs(len(new_favs))
            result_ids = {get_post_id(p) for p in result}
            result = [p for p in result if get_post_id(p) not in old_ids]
            self.logger.info("Loaded %d new posts", len(result))
            new_favs.extend(result)
            if not old_ids.isdisjoint(result_ids) or len(result_ids) == 0:
                break
            sleep(0.5)  # TODO meh
        return new_favs
