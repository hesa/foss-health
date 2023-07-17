
import humanfriendly

def to_int(nr):
    return humanfriendly.parse_size(str(nr).replace(",",""))

