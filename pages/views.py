from django.shortcuts import render, redirect
from django.http import JsonResponse
from .queries import QueryUsers
from icdesign import utils
from icdesign.backends import login_only, update_registration


# Create your views here.
def index(request):
    ic_id = request.session.get('user')
    url_page = 'pages/index.html'
    data = {"ic_id": ic_id}
    # print(data)
    params = QueryUsers.users_get(data)
    print(params)
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
                "title": "Failed",
                "body": "Please fill the form."
            }
            return JsonResponse(params)

        if ic_pass != confirm_ic_pass:
            params = {
                "title": "Failed",
                "body": "Your password are unmatched."
            }
            return JsonResponse(params)
        else:
            data = {"ic_id": ic_id, "ic_name": ic_name, "ic_pass": ic_pass,
                    "date_joined": utils.currentUnixTimeStamp()}
            print("testing")
            print(data)
            obj, q = QueryUsers.users_getsert(data)
            print(obj, q, type(q))
            if q == False:
                title = "Failed"
                message = "Users already exists."
                params = {
                    "title": title,
                    "body": message
                }
                return JsonResponse(params)
            else:
                print("test2")
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
        data = update_registration(request.POST)

        filterQ = {"ic_id": ic_id}
        q = QueryUsers.users_update(filterQ, data)
        if not q:
            title = "Failed"
            message = "Information not updated."
            params = {
                "title": title,
                "body": message
            }
            return JsonResponse(params)

        return render(request, 'pages/profile.html')

    data = {"ic_id": ic_id}
    # print(data)
    params = QueryUsers.users_get(data)
    # print(params)
    return render(request, url_page, params)


def ic_test_info_page(request):
    return render(request, 'pages/ic_test_info.html')


def ic_pre_exam(request):
    return render(request, 'pages/pre_exam.html')


def ic_faqs(request):
    return render(request, 'pages/faqs.html')


@login_only
def profile_page(request):
    ic_id = request.session.get('user')
    url_page = 'pages/profile.html'
    data = {"ic_id": ic_id}
    # print(data)
    params = QueryUsers.users_get(data)
    # print(params)
    return render(request, url_page, params)


def login_page(request):

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
