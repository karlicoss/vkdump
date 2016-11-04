# Installations:

    pip3 setup.py install

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
        * private messages
        * images from private messages?
        * download person't albums?
        * download person's wall, track changes?
       
    * API does not return more that 1000 favs, have to update regularly

    * download images for new favs
