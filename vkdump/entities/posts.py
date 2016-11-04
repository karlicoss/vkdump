def get_post_id(post: dict) -> str:
    return "%d_%d" % (post['owner_id'], post['id'])
