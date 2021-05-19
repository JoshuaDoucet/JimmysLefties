# users/urls.py

from django.conf.urls import url, include
from users.views import dashboard, register, allSearches
urlpatterns = [
    # accounts/login/
    # accounts/logout/
    # accounts/password_change/
    # accounts/password_change/done/
    # accounts/password_reset/
    # accounts/password_reset/done/ 
    # accounts/reset/<uidb64>/<token>/ 
    #     Refer to it by "password_reset_confirm"
    # accounts/reset/done/
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^register/", register, name="register"),
    url('searches/', allSearches, name="searches"),
]