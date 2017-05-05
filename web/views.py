from django.shortcuts import render


def admin(request):
    return render(request, "web/index_admin.html")


def member(request):
    return render(request, "web/index_member.html")


def request_confirmation(request):
    return render(request, "web/request_confirmation.html")


def confirmations(request):
    return render(request, "web/confirmations.html")


def accounts(request):
    return render(request, "web/accounts.html")


def login(request):
    return render(request, "web/login.html")
