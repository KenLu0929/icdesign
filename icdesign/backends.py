from pages.models import Users
from django.shortcuts import redirect
from icdesign import utils

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


def update_registration(data_post):
    print(data_post)
    data = {}
    # personal data
    data["ic_address"] = data_post.get("ic_address", "")
    data["ic_gender"] = data_post.get("ic_gender", "")
    data["ic_email"] = data_post.get("ic_email", "")
    data["ic_address"] = data_post.get("ic_address", "")
    data["ic_bod"] = data_post.get("ic_bod", "")
    data["ic_phone_no"] = data_post.get("ic_phone_no", "")
    data["ic_telephone"] = data_post.get("ic_telephone", "")

    # education data
    data["ic_school"] = data_post.get("ic_school", "")
    data["ic_status_school"] = data_post.get("ic_status_school", "")
    data["ic_degree"] = data_post.get("ic_degree", "")
    data["ic_company"] = data_post.get("ic_company", "")
    data["ic_department"] = data_post.get("ic_department", "")
    data["ic_service_department"] = data_post.get("ic_service_department", "")
    data["ic_job_position"] = data_post.get("ic_job_position", "")
    data["ic_yearofexp"] = data_post.get("ic_yearofexp", "")

    # ic_test = data_post.getlist("ic_test[]", "")
    # for test in ic_test:
    #
    # print(ic_test)
    data["date_modified"] = utils.currentUnixTimeStamp()

    print(data)
    data = utils.remove_dict_key_empty(data)
    print(data)
    return data
