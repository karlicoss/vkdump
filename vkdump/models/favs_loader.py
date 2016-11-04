import json
from pathlib import Path
from time import sleep
from typing import List

from vkdump.api import get_api
from vkdump.config import config
from vkdump.entities.posts import get_post_id


class FavsLoader:
    def __init__(self):
        self.favs_path = config.FAVS  # type: Path
        self.api = get_api()

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
        print(new_favs)
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
            print(result_ids)

            result = [p for p in result if get_post_id(p) not in old_ids]
            new_favs.extend(result)
            print(result)
            if not old_ids.isdisjoint(result_ids) or len(result_ids) == 0:
                break
            sleep(0.5)  # TODO meh
        return new_favs
