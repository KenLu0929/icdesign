from datetime import datetime

from django.core.mail import BadHeaderError, send_mail
import logging
import time
from icdesign import settings
import uuid
from pages.models import ExamLogs

# Get an instance of a logger
logger = logging.getLogger(__name__)


def send_email(subject, message, recipient_list):
    if subject and message and recipient_list:
        try:
            send_mail(subject, message, settings.EMAIL_HOST, recipient_list)
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


def dict_clean(items):
    # checking for dictionary and replacing if None
    # print(items)
    if isinstance(items, dict):

        for key in items:
            if items[key] is None:
                items[key] = ""
            else:
                dict_clean(items[key])

    # checking for list, and testing for each value
    elif isinstance(items, list):
        for val in items:
            dict_clean(val)
    return items


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
    last_logs = ExamLogs.objects.all().order_by('auto_increment_id').last()
    suffix = "0001"
    if last_logs:
        suffix = str(int(last_logs.auto_increment_id) + 1).zfill(4)
    x = uuid.uuid4()
    x = str(x)[:5].upper()
    # ticket = exams_id + x + str(currentUnixTimeStamp()) + suffix
    ticket = exams_id + x + suffix
    return ticket
