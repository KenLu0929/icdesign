from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from .queries import QueryUsers
# from . import session_custom


# Create your views here.


def index(request):
    return render(request, 'pages/index.html')


def registration_page(request):
    if request.method == "POST":
        print(request.POST)
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
            data = {
                "ic_id": ic_id,
                "full_name": ic_name,
                "ic_pass": ic_pass,
            }
            q = QueryUsers.users_getsert(data)
            title = "Success"
            message = "Your registration are success."
            if not q:
                title = "Failed"
                message = "Users already exists."
            params = {
                "title": title,
                "body": message
            }
            return JsonResponse(params)

    params = {}
    url_page = 'pages/registration.html'
    return render(request, url_page, params)
    # if 'user' in request.session:
    #     # print("user is exist")
    #     return render(request, url_page, params)
    # else:
    #     # print("user is not exist")
    #     return redirect('login')

def testRegistration(request):
    return render(request, 'pages/testregistration.html')

def ictestInfo(request):
    return render(request, 'pages/ictestinfo.html')

def profile_page(request):
    params = {}
    url_page = 'pages/profile.html'
    # print("test")
    return render(request, url_page, params)
    # if 'user' in request.session:
    #     # print("user is exist")
    #     print(request.session)
    #     return render(request, url_page, params)
    # else:
    #     # print("user is not exist")
    #     return redirect('login')


def login_page(request):
    if request.method == "POST":

        id = request.POST.get("ic_id", "")
        pwd = request.POST.get("ic_password", "")

        # print("id:", id)
        # print("pwd:", pwd)
        user = authenticate(request=request, username=id, password=pwd)
        # print(user)
        if user is not None:
            # login(request, user)
            # print(user)
            # request.session['user'] = id
            # request.session.modified = True
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
