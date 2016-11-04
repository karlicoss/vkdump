#!/usr/bin/env python3
from pprint import pprint

from vkdump.models.favs_loader import FavsLoader


def main():
    loader = FavsLoader()
    # favs = loader.load_favs()
    # loader.update()
    favs = loader.load_favs()
    for t in [p['text'] for p in favs[:20]]:
        print(t)
        print("===========================")

    # pprint(favs[1])
    # pprint(sort_dict(favs[1]))
    # favs = load_favs()
    # pprint(favs[:10])
    # dates = [f['date'] for f in favs]
    # pprint(dates)
    # print(all(a >= b for a, b in zip(dates, dates[11:])))
    # api = get_api()
    # collect_attaches()
    # favs = fetch_all_favs()
    # with open("favs.json", 'w') as fo: # TODO instead, merge and sort by timestamp?
    #     json.dump(favs, fo, ensure_ascii=False)


if __name__ == '__main__':
    main()
