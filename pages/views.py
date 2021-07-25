from django.shortcuts import render, redirect
from django.http import JsonResponse
from .queries import QueryUsers, QueryExams, QueryExamsLogs, QueryNews
from icdesign import utils
from icdesign.backends import login_only, update_registration, checking_user_taken_exam, update_profile


# Create your views here.
def index(request):
    ic_id = request.session.get('user')
    url_page = 'pages/index.html'
    data = {"ic_id": ic_id}
    # print(data)
    params = QueryUsers.users_get(data)
    params["news_fields"] = QueryNews.news_get()
    # print(params)
    return render(request, url_page, params)


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
                "message": "Please fill the form."
            }
            return JsonResponse(params)

        if ic_pass != confirm_ic_pass:
            params = {
                "error": True,
                "message": "Your password are unmatched."
            }
            return JsonResponse(params)
        else:
            data = {"ic_id": ic_id, "ic_name": ic_name, "ic_pass": ic_pass,
                    "last_login": utils.currentUnixTimeStamp()}
            # print("testing")
            # print(data)
            obj, q = QueryUsers.users_getsert(data)
            # print(obj, q, type(q))
            if q == False:
                params = {
                    "error": True,
                    "message": "Users already exists."
                }
                return JsonResponse(params)
            else:
                # print("test2")
                request.session['user'] = ic_id
                url_page = 'pages/profile.html'
                return render(request, url_page)

    url_page = 'pages/registration.html'
    return render(request, url_page)


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
                "body": "Please select the exams."
            }
            return JsonResponse(params)
        res = checking_user_taken_exam(ic_id, ic_test)
        if res:
            # print("test_registration_page:", res)
            taken_exams = ", ".join(res)
            params = {
                "error": True,
                "title": "Failed",
                "body": f"you already took {taken_exams} exams."
            }
            return JsonResponse(params)
        # print("test_registration_page 2:", res)
        data, exams_list = update_registration(request.POST, ic_id)
        if data == {}:
            params = {
                "error": True,
                "title": "Failed",
                "body": "Some Error Happen please contact admin."
            }
            return JsonResponse(params)

        filterQ = {"ic_id": ic_id}
        q = QueryUsers.users_update(filterQ, data)
        if not q:
            params = {
                "error": True,
                "title": "Failed",
                "body": "Information not updated."
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
    params = QueryUsers.users_get(data)
    exams_data = {
        "exam_is_active": 1,
    }
    params["exams_fields"] = QueryExams.exams_get(exams_data, True)
    # params["exams_fields"] = {"test": "test"}
    # print(params)
    return render(request, url_page, params)


def ic_test_info_page(request):
    ic_id = request.session.get('user')
    url_page = 'pages/ic_test_info.html'
    data = {"ic_id": ic_id}
    # print(data)
    params = QueryUsers.users_get(data)
    # print(params)
    return render(request, url_page, params)


def ic_sponsorship(request):
    ic_id = request.session.get('user')
    url_page = 'pages/sponsorship.html'
    data = {"ic_id": ic_id}
    # print(data)
    params = QueryUsers.users_get(data)
    # print(params)
    return render(request, url_page, params)


def ic_pre_exam(request):
    ic_id = request.session.get('user')
    url_page = 'pages/pre_exam.html'
    data = {"ic_id": ic_id}
    # print(data)
    params = QueryUsers.users_get(data)
    # print(params)
    return render(request, url_page, params)


def ic_faqs(request):
    ic_id = request.session.get('user')
    url_page = 'pages/faqs.html'
    data = {"ic_id": ic_id}
    # print(data)
    params = QueryUsers.users_get(data)
    # print(params)
    return render(request, url_page, params)


@login_only
def profile_page(request):
    ic_id = request.session.get('user')
    url_page = 'pages/profile.html'
    data = {"ic_id": ic_id}
    # print(data)
    params = QueryUsers.users_get(data)
    # print(params)

    exams_filter = {
        "ic_id": ic_id,
    }
    result = QueryExamsLogs.exams_get(exams_filter)
    params["exams_fields"] = result
    return render(request, url_page, params)


@login_only
def profile_modify(request):
    ic_id = request.session.get('user')
    url_page = 'pages/profile_modify.html'
    data = {"ic_id": ic_id}
    # print(data)

    if request.method == "POST":
        filterQ = {"ic_id": ic_id}
        data = update_profile(request.POST)
        q = QueryUsers.users_update(filterQ, data)
        if not q:
            params = {
                "error": True,
                "title": "Failed",
                "body": "Information not updated."
            }
            return JsonResponse(params)

        params = {
            "error": False,
            "title": "Success",
            "body": "Profile Information is updated."
        }
        # print(params)
        return JsonResponse(params)

    params = QueryUsers.users_get(data)

    return render(request, url_page, params)


@login_only
def change_password(request):
    ic_id = request.session.get('user')
    if request.method == "POST":
        print(request.POST)
        ic_pass = request.POST.get("ic_password", "")
        ic_new_repassword = request.POST.get("ic_new_repassword", "")
        ic_new_password = request.POST.get("ic_new_password", "")

        if ic_new_password != ic_new_repassword:
            params = {
                "error": False,
                "title": "Success",
                "body": "Your password are unmatched."
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
                "body": "Your Password is changed."
            }
            return JsonResponse(params)
        else:
            params = {
                "error": True,
                "title": "Failed",
                "body": "Old Password is wrong."
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
                "message": "invalid id or password"
            }
            # print(resp)
            return render(request, 'pages/login.html', resp)

    return render(request, 'pages/login.html')


def logout_page(request):
    try:
        del request.session['user']
    except:
        return redirect('login')
    return redirect('login')
