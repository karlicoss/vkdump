from pathlib import Path
from typing import List

from vkdump.config import config
from vkdump.models.feed_loader import FeedLoader


class WallLoader(FeedLoader):
    def __init__(self):
        wall_path = config.USER_WALL  # type: Path
        super().__init__(wall_path, logger_tag=WallLoader.__name__)

    def _query_new(self, offset: int) -> List[dict]:
        return self.api.get_wall(owner_id=config.USER_ID, offset=offset)