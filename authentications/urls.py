from django.urls import path
from .views import TestView, oauth2_callback_view, login_user

urlpatterns = [
    path("oauth2/login", login_user, name="oauth2_login"),
    path("oauth2/callback/", oauth2_callback_view, name="oauth2_callback"),
    path("test/", TestView.as_view(), name="test"),
]
