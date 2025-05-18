import uuid
from django.conf import settings
from django.db import models

# Create your models here.

class Email(models.Model):
    #unique because we need just 1 time to add Email and verified it.
    email = models.EmailField(unique=True)
    active = models.BooleanField(default= True)
    timestanp = models.DateTimeField(auto_now_add=True)


class EmailVerificationEvent(models.Model):
    parent = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid1)
   
    attemps = models.IntegerField(default=0)
    last_attemp_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null= True
    ) 

    expired = models.BooleanField(default=False)
    expired_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null= True
    )     
    timestamp = models.DateTimeField(auto_now_add=True)


    def get_link(self):
        return f"{settings.BASE_URL}/verfiy/{self.token}/"
