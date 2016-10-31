from bs4 import BeautifulSoup

import json
import re

POST_ID_REGEX = re.compile('wall(.*)')


posts_ids = None
with open("favs.html", 'r') as fo:
    source = fo.read()
    soup = BeautifulSoup(source, 'html.parser')
    items = soup.find_all('div', {'class': "wall_item"})
    # for item in items:
    posts_ids = [POST_ID_REGEX.match(item.attrs['id']).group(1) for item in items]


with open("posts.json", 'w') as fo:
    json.dump(posts_ids, fo)
    # print(posts_ids)
    # for item in items:
    #     # print("==========================")
    #     # print("data-post-id" in str(item))
    #     post_id =
    #     print(post_id)
    #     # print("==========================")
    # print(items[10])
    # print(len(items))