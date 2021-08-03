import mimetypes

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .queries import QueryUsers, QueryExams, QueryExamsLogs, QueryNews
from icdesign import utils
from icdesign import error_messages
from icdesign.backends import login_only, update_registration, checking_user_taken_exam, update_profile, prerequisite_exams

# for pdf rendering/view
from easy_pdf.views import PDFTemplateResponseMixin
from django.views.generic import DetailView


# Create your views here.
def index(request):
    url_page = 'pages/index.html'
    CUS_PARAMS = {
        "ic_id": "",
        "ic_name": "",
    }
    if 'user' in request.session:
        ic_id = request.session.get('user')
        data = {"ic_id": ic_id}
        # print(data)
        CUS_PARAMS = QueryUsers.users_get(data)

    CUS_PARAMS["news_fields"] = QueryNews.news_get()
    # print(params)
    return render(request, url_page, CUS_PARAMS)


def registration_page(request):
    if request.method == "POST":
        # print(request.POST)
        ic_id = request.POST.get("ic_show", "")
        ic_name = request.POST.get("ic_name", "")
        ic_pass = request.POST.get("ic_password", "")
        confirm_ic_pass = request.POST.get("confirm_ic_password", "")
        # print(ic_pass)
        if ic_id == "" or ic_name == "" or ic_pass == "":
            params = {
                "error": True,
                "message": error_messages.PLEASE_FILL_FORM
            }
            return JsonResponse(params)

        if ic_pass != confirm_ic_pass:
            params = {
                "error": True,
                "message": error_messages.UNMATCHED_PASS
            }
            return JsonResponse(params)
        else:
            data = {"ic_id": ic_id, "ic_name": ic_name, "ic_pass": ic_pass,
                    "last_login": utils.currentUnixTimeStamp()}
            # print("testing")
            # print(data)
            if QueryUsers.users_checking_fields_exists({"ic_id": ic_id}):
                params = {
                    "error": True,
                    "message": error_messages.ID_EXIST
                }
                return JsonResponse(params)
            obj, q = QueryUsers.users_getsert(data)
            # print(obj, q, type(q))
            if q == False:
                params = {
                    "error": True,
                    "message": obj
                }
                return JsonResponse(params)
            else:
                # print("test2")
                request.session['user'] = ic_id
                # url_page = 'pages/test_registration.html'
                redirect("test_registration")

    url_page = 'pages/registration.html'
    CUS_PARAMS = {
        "ic_id": "",
        "ic_name": "",
        "title": "",
        "body": "",
    }
    return render(request, url_page, CUS_PARAMS)


@login_only
def test_registration_page(request):
    url_page = 'pages/test_registration.html'
    ic_id = request.session.get('user')

    if request.method == "POST":
        # print(request.POST)

        # checking if user already took the exam
        ic_test = request.POST.getlist("ic_test[]", [])

        if not ic_test:
            params = {
                "error": True,
                "title": "Failed",
                "body": error_messages.SELECT_EXAM
            }
            return JsonResponse(params)
        res = checking_user_taken_exam(ic_id, ic_test)
        if res:
            # print("test_registration_page:", res)
            taken_exams = ", ".join(res)
            params = {
                "error": True,
                "title": "Failed",
                "body": error_messages.TOOK_EXAM + taken_exams
            }
            return JsonResponse(params)

        res = prerequisite_exams(ic_id, ic_test)
        if res:
            # print("test_registration_page:", res)
            params = {
                "error": True,
                "title": "Failed",
                "body": "<hr>".join(res)
            }
            return JsonResponse(params)
        # print("test_registration_page 2:", res)
        data, exams_list = update_registration(request.POST, ic_id)
        if data == {}:
            params = {
                "error": True,
                "title": "Failed",
                "body": error_messages.GENERAL_ERROR
            }
            return JsonResponse(params)

        filterQ = {"ic_id": ic_id}
        q, message = QueryUsers.users_update(filterQ, data)
        if message is not None:
            params = {
                "error": True,
                "title": "Failed",
                "body": message
            }
            return JsonResponse(params)
        if not q:
            params = {
                "error": True,
                "title": "Failed",
                "body": error_messages.NOT_UPDATED_INFO
            }
            return JsonResponse(params)

        params = {
            "error": False,
            "title": "Success",
            "body": exams_list
        }
        # print(params)
        return JsonResponse(params)

    data = {"ic_id": ic_id}
    # print(data)
    CUS_PARAMS = QueryUsers.users_get(data)
    CUS_PARAMS = utils.dict_clean(CUS_PARAMS)
    exams_data = {
        "exam_is_active": 1,
    }
    CUS_PARAMS["exams_fields"] = QueryExams.exams_get(exams_data, True)
    CUS_PARAMS["title"] = ""
    CUS_PARAMS["body"] = ""
    # params["exams_fields"] = {"test": "test"}
    # print(CUS_PARAMS)
    return render(request, url_page, CUS_PARAMS)


def ic_test_info_page(request):
    url_page = 'pages/ic_test_info.html'
    CUS_PARAMS = {
        "ic_id": "",
        "ic_name": "",
    }
    if 'user' in request.session:
        ic_id = request.session.get('user')
        data = {"ic_id": ic_id}
        # print(data)
        CUS_PARAMS = QueryUsers.users_get(data)
    return render(request, url_page, CUS_PARAMS)


def ic_sponsorship(request):
    url_page = 'pages/sponsorship.html'
    CUS_PARAMS = {
        "ic_id": "",
        "ic_name": "",
    }
    if 'user' in request.session:
        ic_id = request.session.get('user')
        data = {"ic_id": ic_id}
        # print(data)
        CUS_PARAMS = QueryUsers.users_get(data)
    return render(request, url_page, CUS_PARAMS)


def ic_pre_exam(request):
    url_page = 'pages/pre_exam.html'
    CUS_PARAMS = {
        "ic_id": "",
        "ic_name": "",
    }
    if 'user' in request.session:
        ic_id = request.session.get('user')
        data = {"ic_id": ic_id}
        # print(data)
        CUS_PARAMS = QueryUsers.users_get(data)
    return render(request, url_page, CUS_PARAMS)


def ic_faqs(request):
    url_page = 'pages/faqs.html'
    CUS_PARAMS = {
        "ic_id": "",
        "ic_name": "",
    }
    if 'user' in request.session:
        ic_id = request.session.get('user')
        data = {"ic_id": ic_id}
        # print(data)
        CUS_PARAMS = QueryUsers.users_get(data)
    return render(request, url_page, CUS_PARAMS)


@login_only
def profile_page(request):
    ic_id = request.session.get('user')
    url_page = 'pages/profile.html'
    data = {"ic_id": ic_id}
    # print(data)
    params = QueryUsers.users_get(data)
    params = utils.dict_clean(params)
    # print(params)

    exams_filter = {
        "ic_id": ic_id,
    }
    result = QueryExamsLogs.exams_get(exams_filter, True)
    # print(params)
    # print(result)
    params["exams_fields"] = result
    params["title"] = ""
    params["body"] = ""
    return render(request, url_page, params)


@login_only
def profile_modify(request):
    ic_id = request.session.get('user')

    # print(request)

    if request.method == "POST":

        filterQ = {"ic_id": ic_id}

        data = update_profile(request.POST)
        # print("testing: ",data)
        q, message = QueryUsers.users_update(filterQ, data)
        if message is not None:
            params = {
                "error": True,
                "title": "Failed",
                "body": message
            }
            return JsonResponse(params)
        if not q:
            params = {
                "error": True,
                "title": "Failed",
                "body": error_messages.NOT_UPDATED_INFO
            }
            return JsonResponse(params)

        params = {
            "error": False,
            "title": "Success",
            "body": error_messages.UPDATED_INFO
        }
        # print(params)
        return JsonResponse(params)

    data = {"ic_id": ic_id}
    params = QueryUsers.users_get(data)
    params = utils.dict_clean(params)
    params["title"] = ""
    params["body"] = ""
    url_page = 'pages/profile_modify.html'
    return render(request, url_page, params)


@login_only
def change_password(request):
    ic_id = request.session.get('user')
    if request.method == "POST":
        # print(request.POST)
        ic_pass = request.POST.get("ic_password", "")
        ic_new_repassword = request.POST.get("ic_new_repassword", "")
        ic_new_password = request.POST.get("ic_new_password", "")

        if ic_new_password != ic_new_repassword:
            params = {
                "error": False,
                "title": "Success",
                "body": error_messages.UNMATCHED_PASS
            }
            return JsonResponse(params)

        filter_sql = {
            "ic_id": ic_id,
            "ic_pass": ic_pass,
        }
        user = QueryUsers.users_get(filter_sql)

        if bool(user):
            updated_data = {
                "ic_pass": ic_new_password,
            }
            QueryUsers.users_update(filter_sql, updated_data)
            params = {
                "error": False,
                "title": "Success",
                "body": error_messages.PASSWORD_CHANGED
            }
            return JsonResponse(params)
        else:
            params = {
                "error": True,
                "title": "Failed",
                "body": error_messages.WRONG_OLD_PASSWORD
            }
            # print(resp)
            return JsonResponse(params)

    return redirect("profile")


def login_page(request):
    ic_id = request.session.get('user')
    # print(ic_id)
    if ic_id is not None:
        return redirect("profile")
    if request.method == "POST":
        # print("test")
        ic_id = request.POST.get("ic_id", "")
        ic_pass = request.POST.get("ic_password", "")
        data = {
            "ic_id": ic_id,
            "ic_pass": ic_pass,
        }
        user = QueryUsers.users_get(data)

        if bool(user):
            # login(request, user)
            # print(user)
            request.session['user'] = ic_id
            request.session.modified = True
            filter_sql = {
                "ic_id": ic_id
            }
            data = {"last_login": utils.currentUnixTimeStamp()}
            QueryUsers.users_update(filter_sql, data)

            return redirect("profile")
        else:
            resp = {
                "error": True,
                "message": error_messages.INVALID_LOGIN
            }
            # print(resp)
            return render(request, 'pages/login.html', resp)

    CUS_PARAMS = {
        "ic_id": "",
        "ic_name": "",
        "error": False,
        "message": "",
    }
    return render(request, 'pages/login.html', CUS_PARAMS)


def logout_page(request):
    try:
        del request.session['user']
    except:
        return redirect('login')
    return redirect('login')


def forget_password(request):
    if request.method == "POST":
        # print("test")
        ic_id = request.POST.get("ic_id", "")
        # print(ic_id)
        data = {
            "ic_id": ic_id,
        }
        user = QueryUsers.users_get(data)

        if bool(user):
            # send to the email
            email = user.get("ic_email", "")
            if email == '':
                resp = {
                    "error": True,
                    "message": error_messages.EMAIL_NOT_REGISTERED
                }
                return JsonResponse(resp)

            utils.send_email(error_messages.SUBJECT_EMAIL_FORGET_PASS, error_messages.BODY_EMAIL_FORGET_PASS + user.get("ic_pass"), [email])
            # print(res)
            resp = {
                "error": False,
                "message": email
            }
            return JsonResponse(resp)
        else:
            resp = {
                "error": True,
                "message": error_messages.ID_NOT_REGISTERED
            }
            return JsonResponse(resp)
    CUS_PARAMS = {
        "ic_id": "",
        "ic_name": "",
        "error": False,
        "message": "",
    }
    return render(request, 'pages/login.html', CUS_PARAMS)


class PDFView(PDFTemplateResponseMixin, DetailView):
    template_name = 'pages/ICLAYOUT_BRIEF.html'
    context_object_name = 'obj'


def ic_privacy(request):
    url_page = 'pages/privacy_notice.html'
    CUS_PARAMS = {
        "ic_id": "",
        "ic_name": "",
        "error": False,
        "message": "",
    }
    if 'user' in request.session:
        ic_id = request.session.get('user')
        data = {"ic_id": ic_id}
        # print(data)
        CUS_PARAMS = QueryUsers.users_get(data)
    return render(request, url_page, CUS_PARAMS)



def download_file_brief(request):
    # fill these variables with real values
    fl_path = 'pages/IC_layout_brief_110.pdf'
    filename = 'IC_layout_brief_110.pdf'
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
    
def download_file_question_bank(request):
    # fill these variables with real values
    fl_path = 'pages/IC_layout_110_question_bank.pdf'
    filename = 'IC_layout_110_question_bank.pdf'
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
