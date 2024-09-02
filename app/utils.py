import hashlib

characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num):
    """ converts hashed value to base62 """
    if num == 0:
        return characters[0]
    base62 = []
    while num > 0:
        num, remainder = divmod(num, 62)
        base62.append(characters[remainder])
    return ''.join(reversed(base62))


def generate_unique_id(url):
    # get hashed url value
    hash_object = hashlib.sha256(str(url).encode())
    hash_int = int(hash_object.hexdigest(), 16)
    short_id = encode_base62(hash_int)[:8]
    return short_id