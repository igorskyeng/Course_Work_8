from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timezone, timedelta

from materials.models import Subscription, Course
from users.models import User


@shared_task
def send_email(pk):
    course = Course.objects.get(pk=pk)
    subscribers = Subscription.objects.get(course=pk)

    send_mail(subject=f'Обновление курса.',
              message=f'В курс "{course}" внесены изменения.',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[subscribers.user.email])


@shared_task
def check_user():
    is_active_users = User.objects.filter(is_active=True)
    current_time = datetime.now(timezone.utc)

    for user in is_active_users:
        if user.last_login:
            if current_time - user.last_login > timedelta(days=30):
                user.is_active = False
                user.save()
