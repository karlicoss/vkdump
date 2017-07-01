from pathlib import Path
from typing import List

from vkdump.config import config
from vkdump.models.feed_loader import FeedLoader


class FavsLoader(FeedLoader):
    def __init__(self):
        favs_path: Path = config.FAVS
        super().__init__(favs_path, logger_tag=FavsLoader.__name__)

    def _query_new(self, offset: int) -> List[dict]:
        return self.api.get_favs(offset=offset)
