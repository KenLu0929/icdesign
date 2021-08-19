from pages.models import Users
from pages.queries import QueryExams, QueryExamsLogs
from django.shortcuts import redirect
from icdesign import utils
from icdesign import error_messages


class CustomBackend(object):

    @staticmethod
    def authenticate(username=None, password=None, **kwargs):

        try:
            user = Users.objects.get(ic_id=username, ic_pass=password)
            return user
        except Users.DoesNotExist:
            return None

    @staticmethod
    def get_user(user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None


def login_only(view_function):
    def wrap(request, *args, **kwargs):
        if 'user' in request.session:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrap


def update_registration(data_post, ic_id):
    # print(data_post)
    data = {
        "ic_address": data_post.get("ic_address", ""),
        "ic_gender": data_post.get("ic_gender", ""),
        "ic_email": data_post.get("ic_email", ""),
        "ic_bod": data_post.get("ic_bod", ""),
        "ic_phone_no": data_post.get("ic_phone_no", ""),
        "ic_telephone": data_post.get("ic_telephone", ""),
        "ic_school": data_post.get("ic_school", ""),
        "ic_status_school": data_post.get("ic_status_school", ""),
        "ic_degree": data_post.get("ic_degree", ""),
        "ic_company": data_post.get("ic_company", ""),
        "ic_department": data_post.get("ic_department", ""),
        "ic_service_department": data_post.get("ic_service_department", ""),
        "ic_job_position": data_post.get("ic_job_position", ""),
        "ic_yearofexp": data_post.get("ic_yearofexp", 0)
    }

    # personal data

    # education data

    ic_test = data_post.getlist("ic_test[]", [])
    exam_list = []
    for exam_id in ic_test:
        # print(exam_id)
        exam = {}
        filter_exam = {"exam_id": exam_id}
        exam_info = QueryExams.exams_get(filter_exam)
        exam["ic_id"] = ic_id
        exam["exam_id"] = exam_id
        # exam["user"] = ic_id
        exam["exam_place"] = exam_info.get("exam_place", "")
        exam["exam_ticket_no"] = utils.generate_exams_ticket(exam_id)
        # print(exam)
        q = QueryExamsLogs.exams_upsert(exam)
        if not q:
            return {}

        exam["exam_start_time"] = exam_info.get("exam_start_time", "")
        exam["exam_end_time"] = exam_info.get("exam_end_time", "")
        exam_list.append(exam)

    # print(data)

    # print(data)
    return data, exam_list


def update_profile(data_post):
    updated_data = {
        "ic_address": data_post.get("ic_address", ""),
        "ic_gender": data_post.get("ic_gender", ""),
        "ic_email": data_post.get("ic_email", ""),
        "ic_bod": data_post.get("ic_bod", ""),
        "ic_phone_no": data_post.get("ic_phone_no", ""),
        "ic_telephone": data_post.get("ic_telephone", ""),
        "ic_school": data_post.get("ic_school", ""),
        "ic_status_school": data_post.get("ic_status_school", ""),
        "ic_degree": data_post.get("ic_degree", ""),
        "ic_company": data_post.get("ic_company", ""),
        "ic_department": data_post.get("ic_department", ""),
        "ic_service_department": data_post.get("ic_service_department", ""),
        "ic_job_position": data_post.get("ic_job_position", ""),
        "ic_yearofexp": data_post.get("ic_yearofexp", 0)
    }

    data = utils.remove_dict_key_empty(updated_data)

    return data


def checking_user_taken_exam(ic_id, exam_list):
    exams_filter = {
        "ic_id": ic_id,
        "exam_finish": False
    }
    taken_exam = []
    result = QueryExamsLogs.exams_get(exams_filter, True)
    for a in result:
        e_id = a.get("exam_id")
        if e_id in exam_list:
            taken_exam.append(e_id)
    # print("checking_user_taken_exam:", result)
    return taken_exam


def prerequisite_exams(ic_id, exam_list):
    unavailable_exams = []
    finish_exams = []
    filter_sql = {
        "ic_id": ic_id,
        "exam_finish": True
    }
    res = QueryExamsLogs.exams_get(filter_sql, True)
    for taken_exams in res:
        finish_exams.append(taken_exams.get("exam_id"))
    # print(finish_exams)
    for exam_id in exam_list:
        filter_exams = {
            "exam_id": exam_id
        }
        exam_res = QueryExams.exams_get(filter_exams)
        prerequisite = exam_res.get("exam_prerequisite")
        # print("prerequisite: ", prerequisite)
        if prerequisite == "-" or prerequisite == "":
            continue
        prerequisite = [x.strip() for x in prerequisite.split(',')]
        # print("arr prerequisite: ", prerequisite)
        # check if users had take the prerequisite exams
        # check = all(item in finish_exams for item in prerequisite)
        preq_exams = []
        for item in prerequisite:
            if item not in finish_exams:
                preq_exams.append(item)

        if preq_exams:
            preq = ",".join(preq_exams)
            # string_msg = f"you cannot take exams {exam_id}{preq}"
            string_msg = error_messages.PREQ_EXAMS_ERR_MESSAGE_PREFIX + exam_id + error_messages.PREQ_EXAMS_ERR_MESSAGE_SUFFIX + preq
            unavailable_exams.append(string_msg)

    return unavailable_exams
