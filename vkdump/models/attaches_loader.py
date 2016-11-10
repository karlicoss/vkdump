import logging
from typing import Dict, List
from urllib.request import urlretrieve

import vkdump.config
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
    def __init__(self) -> None:
        self.config = vkdump.config.config
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

    def _retrieve_photos(self, photos: List[PhotoAttach]):
        for i, a in enumerate(photos):
            u = a.best_url()
            self.logger.info("Retreiving [%d/%d]: %s", i, len(photos), u)
            urlretrieve(u, self.config.IMAGES_DIR.joinpath(a.photo_id()).as_posix())

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
