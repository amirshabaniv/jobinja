from django.core.mail import EmailMessage
import random
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .models import OneTimePassword, Employer
from django.contrib.auth import get_user_model
User = get_user_model()


def send_otp_code(phone_number, request):
    otp = random.randint(1000, 9999)
    employer = Employer.objects.get(phone_number=phone_number)
    OneTimePassword.objects.create(user=employer.user, otp=otp)
    
	# try:
	# 	api = KavenegarAPI('place your kavenegar api key here')
	# 	params = {
	# 		'sender': '',
	# 		'receptor': phone_number,
	# 		'message': f'{otp} کد تایید شما '
	# 	}
	# 	response = api.sms_send(params)
	# 	print(response)
	# except APIException as e:
	# 	print(e)
	# except HTTPException as e:
	# 	print(e)


def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
)
    email.send()