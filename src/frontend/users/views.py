from django.shortcuts import render

# Create your views here.


def current_orders(request):
    context = {"title": "current orders"}
    return render(request, "user/current_orders.html", context)


def archived_orders(request):
    context = {"title": "archived orders"}
    return render(request, "user/archived_orders.html", context)


def create_order(request):
    context = {"title": "create order"}
    return render(request, "user/create_order.html", context)


def profile(request):
    context = {"title": "profile"}
    return render(request, "user/profile_form.html", context)


def add_users(request):
    context = {
        'title': 'add users'
    }
    return render(request, "user/add_users.html", context)

def add_drugs(request):
    context = {
        'title': 'add drugs'
    }
    return render(request, "user/add_drugs.html", context)

