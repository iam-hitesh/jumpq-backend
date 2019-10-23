import uuid

from jumpq.celery import celery_app as current_app
import users.models

@current_app.task()
def send_sms(mobile, text):
    print(text)

def generate_referral_code():
    not_unique = True
    while not_unique:
        referral_code = uuid.uuid4().hex[:6].upper()

        if not users.models.User.objects.filter(referral_code=referral_code).exists():
            not_unique = False

    return referral_code