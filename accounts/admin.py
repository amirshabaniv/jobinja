from django.contrib import admin
from .models import JobSeeker, Employer, OneTimePassword
from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.register(User)

admin.site.register(OneTimePassword)

admin.site.register(JobSeeker)

admin.site.register(Employer)
