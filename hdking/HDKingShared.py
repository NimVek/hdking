import logging

LOG_LEVEL = logging.DEBUG
logging.basicConfig()
log = logging.getLogger('hdking')
log.setLevel(LOG_LEVEL)


class HDKingException(Exception):
    pass


def HDKingAssert(condition, msg):
    if not condition:
        raise HDKingException(msg)
