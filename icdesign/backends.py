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
    data["ic_courses"] = data_post.get("ic_courses", "")
    data["ic_gender"] = data_post.get("ic_gender", "")
    data["ic_email"] = data_post.get("ic_email", "")
    data["ic_school"] = data_post.get("ic_school", "")
    data["ic_address"] = data_post.get("ic_address", "")
    data["ic_department"] = data_post.get("ic_department", "")
    data["ic_statusSchool"] = data_post.get("ic_statusSchool", "")
    data["company_name"] = data_post.get("ic_company", "")
    data["ic_status"] = data_post.get("ic_status", "")
    data["ic_yearofexp"] = data_post.get("ic_yearofexp", "")
    data["ic_title"] = data_post.get("ic_title", "")
    data["highest_degree"] = data_post.get("ic_degree", "")
    print(data)
    data = utils.remove_dict_key_empty(data)
    print(data)
    return data_post
