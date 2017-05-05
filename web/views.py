from django import urls
from django.contrib.auth import authenticate
from django.contrib.auth import login as save_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def admin(request):
    return render(request, "web/index_admin.html")


@login_required(login_url="/login/")
def member(request):
    context = {}
    return render(request, "web/index_member.html", context=context)


def request_confirmation(request):
    return render(request, "web/request_confirmation.html")


def confirmations(request):
    return render(request, "web/confirmations.html")


def accounts(request):
    return render(request, "web/accounts.html")


def login(request):
    if request.user.is_authenticated:
        return redirect(urls.reverse(member))
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            save_login(request, user)
            return redirect(urls.reverse(member))

        if username or password:
            context = {"error_message": "Username/password combination is incorrect. Please try again!"}

    return render(request, "web/login.html", context=context)
