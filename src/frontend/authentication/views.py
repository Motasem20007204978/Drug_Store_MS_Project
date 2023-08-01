from django.shortcuts import render

# Create your views here.


def home(request):
    context = {
        "title": "home",
    }
    return render(request, "base/landing_page.html", context=context)


def login(request):
    context = {
        "title": "login",
    }
    return render(request, "auth/login.html", context=context)


def reset_password(request):
    context = {
        "title": "verify",
    }
    return render(request, "auth/reset_pass.html", context=context)


def set_password(request):
    context = {
        "title": "set password",
    }
    return render(request, "auth/set_pass.html", context=context)


def change_password(request):
    context = {
        "title": "change password",
    }
    return render(request, "auth/change_pass.html", context=context)


def pyscritp(request):
    return render(request, "pyscript.html")
