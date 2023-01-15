from __future__ import absolute_import, unicode_literals

from celery import shared_task
from rest_framework.generics import get_object_or_404
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string


@shared_task(name="delete_expired_tokens")
def delete_expired_tokens():
    call_command(command_name="flushexpiredtokens")


@shared_task(name="send_login_password")
def send_password(email):
    User = get_user_model()
    user = get_object_or_404(User, email=email)
    subject = 'login site password'
    message = f'the password for loging in your homepage is \n {user.password}'
    # Render the HTML template with sample data
    html_message = render_to_string(
        "mail_templates/login_password.html", {"message": message}
    )
    user.email_user(subject, "", html_message=html_message)
    return f"email activation is sent"

