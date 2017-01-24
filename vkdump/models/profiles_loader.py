import datetime
import json
import logging
from pathlib import Path
from typing import List

from atomicwrites import atomic_write

from vkdump.api import get_api
from vkdump.config import config


class ProfilesLoader:
    def __init__(self):
        self.api = get_api()
        self.logger = logging.getLogger(ProfilesLoader.__name__)

    def update_all(self, ids: List[str]):
        profiles = self.api.get_several(ids)
        for p in profiles:
            self._save_profile(p)

    def _save_profile(self, profile: dict):
        id_ = str(profile['id'])  # jeez, why is it int?
        profiles_dir = config.WALLS_DIR.joinpath(id_).joinpath('profiles')  # type: Path
        if not profiles_dir.exists():
            self.logger.warning("Directory %s doesn't exist; creating", profiles_dir.as_posix())
            profiles_dir.mkdir()
        now = datetime.datetime.now()
        timestamp = int(now.timestamp())
        # isoformat is for human readable file names
        profile_file = profiles_dir.joinpath("profile_%d_%s.json" % (timestamp, now.date().isoformat()))
        with atomic_write(profile_file.as_posix(), overwrite=True) as fo:
            # TODO deduplication
            json.dump(profile, fo, indent=4, ensure_ascii=False, sort_keys=True)
