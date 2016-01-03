#!/usr/bin/env python3
import json
from pprint import pprint

import config

import vk

from api.friends import get_friends
from api.users import get_single, get_subscriptions

session = vk.Session()

api = vk.API(session)


def print_json(jdict):
    print(json.dumps(jdict, indent=4))

# entities
# https://vk.com/dev/datatypes

# pprint(get_single(user_id=config.USER_ID))

# print_json(get_subscriptions(user_id=config.USER_ID))
print_json(get_friends(user_id=config.USER_ID))
# methods
# https://vk.com/dev/methods