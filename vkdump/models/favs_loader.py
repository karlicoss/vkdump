import logging
from pathlib import Path

from typing import List

from vkdump.api import get_api
from vkdump.config import config
from vkdump.models.attaches_loader import AttachesLoader
from vkdump.models.feed_loader import FeedLoader


class FavsLoader(FeedLoader):
    def __init__(self, ):
        favs_path = config.FAVS  # type: Path
        super().__init__(favs_path)
        self.api = get_api()
        self.attaches_loader = AttachesLoader()
        self.logger = logging.getLogger(FavsLoader.__name__)

    def _query_new(self, offset: int) -> List[dict]:
        return self.api.get_favs(offset=offset)
