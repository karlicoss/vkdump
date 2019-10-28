from pathlib import Path

from typing import Dict, List, Any, NamedTuple



class Config(NamedTuple):
    USER_ID: str
    ACCESS_TOKEN: str
    FAVS: Path
    WALLS_DIR: Path
    IDS_TO_DUMP: List[str]

    @classmethod
    def from_path(cls, path: Path):
        # I know it's not very safe, but couldn't find any decent configuration format for Python
        # supporting dicts
        # Anyway, if user adds some bad code in configuration.py, it's their problem :)
        result: Dict[str, Any] = {}
        with path.open('r') as fo:
            exec(fo.read(), result)
        dct = {}
        for attr in cls._fields:
            dct[attr] = result[attr]
        return cls(**dct)


config: Config
try:
    config = Config.from_path(Path('configuration.py'))
    for v in vars(config):
        globals()[v] = getattr(config, v)
except Exception as e:
    import sys

    sys.stderr.write("[Config] Error while reading configuration file: " + str(e))

__all__ = ['config']
