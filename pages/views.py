from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from . import session_custom


# Create your views here.


def index(request):
    return render(request, 'pages/index.html')


def registration_page(request):
    params = {}
    url_page = 'pages/registration.html'
    if 'user' in request.session:
        # print("user is exist")
        return render(request, url_page, params)
    else:
        # print("user is not exist")
        return redirect('login')


def profile_page(request):
    params = {}
    url_page = 'pages/profile.html'
    # print("test")
    if 'user' in request.session:
        # print("user is exist")
        print(request.session)
        return render(request, url_page, params)
    else:
        # print("user is not exist")
        return redirect('login')


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
            print(user)
            request.session['user'] = id
            request.session.modified = True
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
