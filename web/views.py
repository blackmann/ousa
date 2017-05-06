from django import urls
from django.contrib.auth import authenticate
from django.contrib.auth import login as save_login
from django.contrib.auth import logout as logout_session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone

from web.models import ConfirmationRequest, Contribution, Admin


def invalid_amount(amount):
    return not amount or int(amount) < 1


def is_admin(user):
    return Admin.objects.filter(member=user, is_admin=True).exists()


@login_required(login_url="/login/")
def admin(request):
    context = {}
    if request.user.is_authenticated:
        if is_admin(request.user):
            context = {"not_authorized": False}
        else:
            context = {"not_authorized": True}
    return render(request, "web/index_admin.html", context=context)


@login_required(login_url="/login/")
def member(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        contributions = Contribution.objects.filter(member=user)
        total_contributions = sum([c.amount for c in contributions if c.approved])
        context = {"contributions": contributions, "total_contributions": total_contributions}
    return render(request, "web/index_member.html", context=context)


@login_required(login_url="/login/")
def request_confirmation(request):
    context = {}
    if request.method == "POST":
        amount = request.POST["amount"]
        reference = request.POST["reference"]
        merchant = request.POST["merchant"]

        if (not invalid_amount(amount)) and request.user.is_authenticated:
            user = request.user
            confirmation_request = ConfirmationRequest()
            contribution = Contribution()
            contribution.member = user
            contribution.amount = amount
            contribution.save()

            confirmation_request.contribution = contribution
            confirmation_request.merchant = merchant
            confirmation_request.reference = reference

            confirmation_request.save()
            return redirect(urls.reverse(member))

        else:
            context = {"error_message": "Amount field is required. Should be more than 0"}

    return render(request, "web/request_confirmation.html", context=context)


@login_required(login_url="/login/")
def confirmations(request):
    if not is_admin(request.user):
        return redirect(urls.reverse(admin))
    unapproved_confirmations = ConfirmationRequest.objects.filter(approved=False)
    context = {"unapproved_confirmations": unapproved_confirmations}

    return render(request, "web/confirmations.html", context=context)


def get_contribution(user):
    return sum([c.amount for c in Contribution.objects.filter(member=user, approved=True)])


@login_required(login_url="/login/")
def accounts(request):
    if not is_admin(request.user):
        return redirect(urls.reverse(admin))
    all_accounts = [{"name": member.get_full_name(), "contribution": get_contribution(member)}
                    for member in User.objects.all()]

    context = {"accounts": all_accounts}
    return render(request, "web/accounts.html", context=context)


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


def logout(request):
    logout_session(request)
    return redirect(urls.reverse(login))


@login_required(login_url="/login/")
def delete_request(request, pk):
    confirmation_request = ConfirmationRequest.objects.get(pk=pk)
    if request.method == "POST":
        if int(request.POST["delete"]) == 1:
            confirmation_request.contribution.delete()
            confirmation_request.delete()
        return redirect(urls.reverse(member))
    context = {"confirmation_request": confirmation_request}
    return render(request, "web/delete_request.html", context=context)


@login_required(login_url="/login/")
def request_detail(request, pk):
    if not is_admin(request.user):
        return redirect(urls.reverse(admin))
    confirmation_request = ConfirmationRequest.objects.get(pk=pk)
    if request.method == "POST":
        confirm = request.POST["confirm"]
        if int(confirm) == 1:
            confirmation_request.approved = True
            confirmation_request.save()

            contribution = confirmation_request.contribution
            contribution.approved = True
            contribution.date_approved = timezone.now()
            contribution.save()
        return redirect(urls.reverse(confirmations))
    context = {"conf_req": confirmation_request}
    return render(request, "web/request_detail.html", context=context)
