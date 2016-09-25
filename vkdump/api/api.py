import vk

VK_API_VERSION = '5.42'


# TODO: limits
class ApiHolder(object):
    def __init__(self):
        super().__init__()
        self.api = vk.API(vk.Session())


def get_api_holder():
    return ApiHolder()


def get_api():
    return get_api_holder().api
