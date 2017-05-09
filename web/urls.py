from django.conf.urls import url

from web import views

urlpatterns = [
    url(r"admin-panel", views.admin, name="admin_panel"),
    url(r"member", views.member, name="member"),
    url(r"request-confirmation", views.request_confirmation, name="request_confirmation"),
    url(r"confirmations", views.confirmations, name="confirmations"),
    url(r"login", views.login, name="login"),
    url(r"accounts", views.accounts, name="accounts"),
    url(r"logout", views.logout, name="logout"),
    url(r"delete_request/(\d+)", views.delete_request, name="delete_request"),
    url(r"request_detail/(\d+)", views.request_detail, name="request_detail"),
    url(r"^$", views.member, name="index"),
]
