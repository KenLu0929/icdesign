from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .queries import QueryUsers
from icdesign import utils


# from . import session_custom


# Create your views here.
def index(request):
    return render(request, 'pages/index.html')


def registration_page(request):
    url_page = 'pages/registration.html'
    if request.method == "POST":
        # print(request.POST)
        ic_id = request.POST.get("ic_show", "")
        ic_name = request.POST.get("ic_name", "")
        ic_pass = request.POST.get("ic_password", "")
        confirm_ic_pass = request.POST.get("confirm_ic_password", "")
        # print(ic_pass)
        if ic_pass != confirm_ic_pass:
            params = {
                "title": "Failed",
                "body": "Your password are unmatched."
            }
            return JsonResponse(params)
        else:
            data = {"ic_id": ic_id, "full_name": ic_name, "ic_pass": ic_pass,
                    "date_joined": utils.currentUnixTimeStamp()}
            obj, q = QueryUsers.users_getsert(data)
            # title = "Success"
            # message = "Your registration are success."
            if not q:
                title = "Failed"
                message = "Users already exists."
                params = {
                    "title": title,
                    "body": message
                }
                return JsonResponse(params)
            request.session['user'] = ic_id
            return render(request, url_page, obj)

    return render(request, url_page)


def test_registration_page(request):
    url_page = 'pages/test_registration.html'
    if 'user' in request.session:
        ic_id = request.session['user']
        if request.method == "POST":

            data = {"ic_id": ic_id}
            q = QueryUsers.users_upsert(data)
            if not q:
                title = "Failed"
                message = "Information not updated."
                params = {
                    "title": title,
                    "body": message
                }
                return JsonResponse(params)

            return render(request, 'pages/profile.html')

        return render(request, url_page)
    else:
        # print("user is not exist")
        return redirect('login')


def ic_test_info_page(request):
    return render(request, 'pages/ic_test_info.html')


def profile_page(request):
    if 'user' in request.session:
        ic_id = request.session['user']
        url_page = 'pages/profile.html'
        data = {"ic_id": ic_id}
        print(data)
        params = QueryUsers.users_get(data)
        print(params)
        return render(request, url_page, params)
    else:
        # print("user is not exist")
        return redirect('login')


def login_page(request):
    if request.method == "POST":

        ic_id = request.POST.get("ic_id", "")
        pwd = request.POST.get("ic_password", "")
        user = authenticate(request=request, username=ic_id, password=pwd)
        if user is not None:
            # login(request, user)
            # print(user)
            request.session['user'] = ic_id
            request.session.modified = True
            data = {"ic_id": ic_id, "last_login": utils.currentUnixTimeStamp()}
            QueryUsers.users_upsert(data)

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
