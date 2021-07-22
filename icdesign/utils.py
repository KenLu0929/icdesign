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
    result = [{k: v for k, v in d.items() if v and v.strip()} for d in listDict]
    return result