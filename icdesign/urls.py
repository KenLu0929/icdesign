"""icdesign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from pages import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="homepage"),
    path('registration/', views.registration_page, name="registration"),
    path('login/', views.login_page, name="login"),
    path('profile/', views.profile_page, name="profile"),
    path('testregistration/', views.test_registration_page, name="test_registration"),
    path('ictestinfo/', views.ic_test_info_page, name="ic_test_info"),
]
