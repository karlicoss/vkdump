from pathlib import Path
from typing import List

from vkdump.api.api import is_deleted

from vkdump.config import config
from vkdump.models.feed_loader import FeedLoader


class WallLoader(FeedLoader):
    def __init__(self, uid: str) -> None:
        wall_path: Path = config.WALLS_DIR.joinpath(uid)
        super().__init__(wall_path, logger_tag=WallLoader.__name__ + "_" + uid)
        self.uid = uid

    # TODO actually, on network error should be (fairly) safe to be defensive and just return empty list as well..
    def _query_new(self, offset: int) -> List[dict]:
        try:
            return self.api.get_wall(owner_id=self.uid, offset=offset)
        # TODO same logic should be for other loaders
        except Exception as e:
            if is_deleted(e):
                # nothing we can do!
                self.logger.warning(str(e))
                return []
            else:
                raise e
