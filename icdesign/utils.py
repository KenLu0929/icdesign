from django.core.mail import BadHeaderError, send_mail
from .global_variables import ADMIN_EMAIL
import logging
import time

# Get an instance of a logger
logger = logging.getLogger(__name__)


def send_email(subject, message, recipient_list):

    if subject and message and recipient_list:
        try:
            send_mail(subject, message, ADMIN_EMAIL, recipient_list)
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
