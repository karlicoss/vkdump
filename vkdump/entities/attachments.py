from typing import Dict


class PhotoAttach:
    def __init__(self) -> None:
        self.json: Dict = None

    def text(self) -> str:
        return self.json['text']

    def photo_id(self) -> str:
        owner_id = self.json['owner_id']
        p_id = self.json['id']
        return "%d_%d" % (owner_id, p_id)

    def best_url(self):
        sizes = {
            int(k[6:]): v for k, v in self.json.items() if k.startswith('photo_')
        }
        p = max(sizes.items(), key=lambda p: p[0])[1]
        return p

    @staticmethod
    def from_json(json: Dict) -> 'PhotoAttach':
        type = 'photo'
        if json['type'] != type:
            raise AssertionError
        photo_json = json[type]
        attach = PhotoAttach()
        attach.json = photo_json
        return attach

    def __str__(self):
        d = {
            'text': self.text(),
            'photo_id': self.photo_id(),
            'best_url': self.best_url(),
        }
        return str(d)

