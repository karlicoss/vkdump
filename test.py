import logging

# blogger = logging.getLogger('backoff')
# blogger.addHandler(logging.StreamHandler())
# blogger.setLevel(logging.FATAL)

# TODO ugh. do not use basicConfig, it's doing something stupid..
# logging.basicConfig(level=logging.INFO)

import coloredlogs # type: ignore
# TODO this triggers default logging for stuff without handlers. what the fuck??
# fuck that complicated format, easier without it
# coloredlogs.install(fmt="%(asctime)s [%(name)s] %(levelname)s %(message)s")

# from kython import get_logzero
# get_logzero('')

# this is deleted user
# we only get api errors on him, so ideally should bail immediately

# firejail --noprofile --net=none python3 test.py 

# like that, should bail immediately
# under firejail, should give up after retries
def test_logging():
    from vkdump.models.wall_loader import WallLoader
    DELETED_ID = '16967694'
    loader = WallLoader(DELETED_ID)
    loader._get_new_posts([])

test_logging()

# TODO python decorator to mess with network??
# from vkdump.models.profiles_loader import ProfilesLoader

# from vkdump.__main__ import update_profiles

# loader = ProfilesLoader()

# loader.update_all(['1303659'])
# update_profiles()
