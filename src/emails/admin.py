from django.contrib import admin

# Register your models here.
from .models import EmailVerificationEvent, Email

admin.site.register(Email)
admin.site.register(EmailVerificationEvent)