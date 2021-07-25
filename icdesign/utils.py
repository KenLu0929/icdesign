from datetime import datetime

from django.core.mail import BadHeaderError, send_mail
import logging
import time
from icdesign import settings
import uuid

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


# %Y-%m-%d%
def date_string_date(date_string):
    date_time_obj = datetime.strptime(date_string, settings.DATE_FORMAT)
    return date_time_obj


def get_fields_only(data):
    # print(data)
    new_data = []
    for a in data:
        # print(a)
        new_data.append(a.get("fields"))
    # print(new_data)
    return new_data


def generate_exams_ticket(exams_id):
    x = uuid.uuid4()
    x = str(x)[:7].upper()
    ticket = exams_id+x+str(currentUnixTimeStamp())
    return ticket
