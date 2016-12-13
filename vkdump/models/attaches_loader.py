import logging
import os
from pathlib import Path
from typing import Dict, List
from urllib.error import HTTPError
from urllib.request import urlretrieve

from vkdump.entities.attachments import PhotoAttach

_IGNORED_TYPES = {
    'audio',
    'doc',
    'page',
    'video',

    'photos_list',  # wtf is that?
    'posted_photo',  # wtf?
    'album',  # there is only one album, screw it
    'note',  # there are few, but later TODO

    'poll',  # later TODO
    'link',  # not really necessary, they are embedded
    'graffiti',  # well, six graffitis, maybe later
}

_TYPES = {
    'photo',
}


class AttachesLoader:
    def __init__(self, images_dir: Path) -> None:
        self.images_dir = images_dir  # type: Path
        # TODO create if not existnent?
        self.logger = logging.getLogger(AttachesLoader.__name__)

    def _get_attachments(self, fav: Dict[str, List[Dict]]) -> List[Dict]:
        attaches = fav.get('attachments', [])
        att = []
        for a in attaches:
            t = a['type']
            if t not in _TYPES and t not in _IGNORED_TYPES:
                self.logger.error("Unexpected type: " + t + " in " + str(fav))
            if t in _TYPES:
                att.append(a)
        return att

    def __get_photo(self, url: str, path: Path):
        if not self.images_dir.exists():
            self.logger.warn("Directory %s doesn't exist; creating", self.images_dir.as_posix())
            os.makedirs(self.images_dir.as_posix(), exist_ok=True)
        try:
            urlretrieve(url, path.as_posix())
        except HTTPError as e:
            if e.code == 502:  # bad gateway
                self.logger.error(str(e))
            else:
                raise e

    def _retrieve_photos(self, photos: List[PhotoAttach]):
        for i, a in enumerate(photos):
            u = a.best_url()
            self.logger.info("Retrieving [%d/%d]: %s", i, len(photos), u)
            self.__get_photo(u, self.images_dir.joinpath(a.photo_id()))

    def download_attaches(self, favs: List[Dict]) -> None:
        attaches = {}  # type: Dict
        for fav in favs:
            att = self._get_attachments(fav)
            for a in att:
                t = a['type']
                l = attaches.get(t, [])
                l.append(a)
                attaches[t] = l

        photos = [PhotoAttach.from_json(json) for json in attaches.get('photo', [])]
        self._retrieve_photos(photos)
