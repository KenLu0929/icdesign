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
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="homepage"),
    path('registration', views.registration_page, name="registration"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
    path('profile', views.profile_page, name="profile"),
    path('profilemodify', views.profile_modify, name="profile_modify"),
    path('changepassword', views.change_password, name="change_password"),
    path('testregistration', views.test_registration_page, name="test_registration"),
    path('ictestinfo', views.ic_test_info_page, name="ic_test_info"),
    path('preexam', views.ic_pre_exam, name="ic_pre_exam"),
    path('faqs', views.ic_faqs, name="ic_faqs"),
    path('sponsorship', views.ic_sponsorship, name="ic_sponsorship"),
    path('privacy', views.ic_privacy, name="ic_privacy"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# print(urlpatterns)