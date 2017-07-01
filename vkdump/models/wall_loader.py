from pathlib import Path
from typing import List

from vkdump.config import config
from vkdump.models.feed_loader import FeedLoader


class WallLoader(FeedLoader):
    def __init__(self, uid: str) -> None:
        wall_path: Path = config.WALLS_DIR.joinpath(uid)
        super().__init__(wall_path, logger_tag=WallLoader.__name__ + "_" + uid)
        self.uid = uid

    def _query_new(self, offset: int) -> List[dict]:
        return self.api.get_wall(owner_id=self.uid, offset=offset)
