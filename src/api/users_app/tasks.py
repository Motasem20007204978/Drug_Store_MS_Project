from __future__ import absolute_import, unicode_literals

from urllib import parse

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.management import call_command
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404

User = get_user_model()

def email_user(email, subject, template, data):
    html_message = render_to_string(f"mail_templates/{template}", data)
    send_mail(
        subject,
        "",
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message,
    )


@shared_task(name="send_login_password")
def send_password(email, password):
    subject = "login site password"
    message = f"the password for logging in your homepage is \n {password}"
    email_user(
        email, subject, "login_password.html", data={"message": message}
    )
    return f"email activation is sent"


def make_activation_url(url_name, uuid64, token):
    qd = {"uuid": uuid64, "token": token}
    qp = parse.urlencode(qd)
    site = Site.objects.get_current()
    current_domain = site.domain
    relative_url = reverse(url_name)
    activation_link = f"http://{current_domain}{relative_url}?{qp}"
    return activation_link


@shared_task(name="send_email_activation")
def send_activation(data):
    email = data.get("email", "")
    user = get_object_or_404(User, email=email)
    uuid = user.generate_uuid()
    token = user.generate_token()
    url_name = data.get("url_name", "activate-user")
    url = make_activation_url(url_name, uuid, token)
    subject = "email activation link"
    message = f"checking email url"
    email_user(
        email,
        subject,
        "activation_link.html",
        data={"message": message, "link": url},
    )
    return f"email activation is sent"
