#!/usr/bin/env python3
import json

from vkdump.api import get_api
from vkdump.config import config


def main():
    api = get_api()

    def print_json(jdict):
        print(json.dumps(jdict, indent=4))

    # entities
    # https://vk.com/dev/datatypes

    # pprint(get_single(user_id=config.USER_ID))

    # print_json(get_subscriptions(user_id=config.USER_ID))
    print_json(api.get_friends(user_id=config.USER_ID))
    # methods
    # https://vk.com/dev/methods


if __name__ == '__main__':
    main()
