from django.core.mail import BadHeaderError, send_mail
import logging
import time

# Get an instance of a logger
logger = logging.getLogger(__name__)


def send_email(subject, message, recipient_list):

    if subject and message and recipient_list:
        try:
            send_mail(subject, message, "", recipient_list)
        except BadHeaderError:
            logger.error('Invalid header found.')
            return False
        return True
    else:
        # In reality we'd use a form class
        # to get proper validation errors.f
        logger.error('Make sure all fields are entered and valid.')
        return False


def currentUnixTimeStamp():
    unixTime = int(time.time())
    return unixTime


def remove_dict_key_empty(listDict):
    clean = {}
    for k, v in listDict.items():
        if isinstance(v, dict):
            nested = remove_dict_key_empty(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean
