This script backs up your VK.com favorites and your wall to a JSON file + images in a separate directory.

# Installation:

    git clone git@github.com:karlicoss/vkdump.git
    cd vkdump
    sudo python3 setup.py install
    cp configuration.py.example configuration.py
    
Now, edit `configuration.py` and set up paths; your id and token (TODO manual for token).
Do not commit this file! Afterwards:

    python3 -m vkdump

# Running tests

    TODO
    
# Typechecking

    mypy vkdump

# TODOs:

* get API token https://vk.com/dev/authcode_flow_user
* handle vk.exceptions.VkAPIError:
* tests (maybe only for DB sanity)
* decide on the storage type (sqlite via dataset?)
    * apparently, json file is fine, there are about 10Mb of favs
* features:
    * tracking friends, to see follow/unfollow dynamics
    * track user info of people you are friends to/follow
    * extract public pages completely
    * download person't albums?
    * download person's wall, track changes?

# Misc:

* API does not return more that 1000 favs, have to update regularly
* for messages, try https://github.com/Totktonada/vk_messages_backup