from datetime import datetime

from django.core.mail import BadHeaderError, send_mail
import logging
import time

from django.db.models import F

from icdesign import settings
import uuid
from pages.models import CounterExamsLogs, Exams
from pages import queries

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
    """ current UnixTime Stamp(conversion type to int)

    Returns:
        int: current UnixTime Stamp
    """

    unixTime = int(time.time())
    return unixTime


def remove_dict_key_empty(listDict):
    """_summary_

    Args:
        listDict (): _description_

    Returns:
        _type_: _description_
    """

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
    """replacing None to "" (use recursive)

    Args:
        items (dict or list): object is replaced

    Returns:
        any: not dict or not list
    """

    if isinstance(items, dict):

        for key in items:
            if items[key] is None:
                items[key] = ""
            else:
                dict_clean(items[key])

    elif isinstance(items, list):
        for val in items:
            dict_clean(val)
    return items


# %Y-%m-%d%
def date_string_date(date_string):
    date_time_obj = datetime.strptime(date_string, settings.DATE_FORMAT)
    return date_time_obj


def get_fields_only(data):
    """ Get value of fields from parameter and return

    Args:
        list : Data with fields

    Returns:
        list : value of fields
    """    
    
    new_data = []
    for a in data:
        new_data.append(a.get("fields"))

    return new_data


def generate_exams_ticket(exams_id):
    last_logs = CounterExamsLogs.objects.all().order_by('auto_increment_id').last()
    suffix = "0001"
    if last_logs:
        suffix = str(int(last_logs.auto_increment_id) + 1).zfill(4)
    x = uuid.uuid4()
    x = str(x)[:5].upper()
    # ticket = exams_id + x + str(currentUnixTimeStamp()) + suffix
    ticket = exams_id + x + suffix

    return ticket


def generate_exams_ticket_v2():
    last_logs = CounterExamsLogs.objects.all().order_by('auto_increment_id').last()
    prefix = "EXAM"
    suffix = "0001"
    if last_logs:
        suffix = str(int(last_logs.auto_increment_id) + 1).zfill(4)
    x = uuid.uuid4()
    x = str(x)[:5].upper()
    # ticket = exams_id + x + str(currentUnixTimeStamp()) + suffix
    ticket = prefix + x + suffix
    res = queries.QueryCounterExamsLogs.users_upsert()
    if not res:
        logger.error("cannot increment counterExamsLogs.")
    return ticket


def generate_admission_ticket(exam_id):
    file_exams = {
        "exam_id": exam_id
    }
    exam = queries.QueryExams.exams_get(file_exams)
    logger.info(exam)
    if exam.get("exam_start_time") is None or str(exam.get("exam_start_time")) == "":
        logger.error("exam_id: " + str(exam_id))
        return "-"
    date_time_obj = datetime.strptime(str(exam.get("exam_start_time")), '%Y-%m-%dT%H:%M:%S')
    first = date_time_obj.strftime("%m%d")
    # print(first)
    second = exam.get("exam_user_taken")
    second = str(second + 1).zfill(2)

    # print(second)

    admission_ticket = first + str(second)
    # print(admission_ticket)
    Exams.objects.filter(exam_id=exam_id).update(exam_user_taken=F('exam_user_taken') + 1)

    return admission_ticket
