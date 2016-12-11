from pathlib import Path
from typing import Any

from typing import Dict


class Config:
    def __init__(self):
        self.USER_ID = None  # str
        self.ACCESS_TOKEN = None  # str
        self.FAVS = None  # Path
        self.USER_WALL = None  # Path

    @staticmethod
    def from_path(path: Path):
        config = Config()
        # I know it's not very safe, but couldn't find any decent configuration format for Python
        # supporting dicts
        # Anyway, if user adds some bad code in configuration.py, it's his problem :)
        result = {}  # type: Dict[str, Any]
        with path.open('r') as fo:
            exec(fo.read(), result)
        for attr in vars(config):
            setattr(config, attr, result[attr])
        return config


config = None  # type: Config
try:
    config = Config.from_path(Path('configuration.py'))
    for v in vars(config):
        globals()[v] = getattr(config, v)
except Exception as e:
    import sys

    sys.stderr.write("[Config] Error while reading configuration file: " + str(e))

__all__ = ['config']
