#!/usr/bin/env python3
from pprint import pprint

import config

import vk

from api.users import get_single

session = vk.Session()

api = vk.API(session)


# entities
# https://vk.com/dev/datatypes

pprint(get_single(user_id=config.USER_ID))
# methods
# https://vk.com/dev/methods