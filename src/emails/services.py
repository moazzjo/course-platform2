from django.conf import settings
from django.core.mail import send_mail 
from django.utils import timezone
from .models import Email, EmailVerificationEvent

EMAIL_HOST_USER = settings.EMAIL_HOST_USER

def verify_email(email):
    qs = Email.objects.filter(email = email, active = False)
    return qs.exists()

def get_verification_email_msg(verification_instance, as_html = False):
    if not isinstance(verification_instance, EmailVerificationEvent):
        return None
    
    verify_link = verification_instance.get_link()

    html_link =f"""
    <h1>Verfiy Your Email by the link:</h1>
    <h2><a href= "{verify_link}">click here</a></h2>
    """
    normal_link = f"""
    Verfiy Your Email by the link: {verify_link}
    """
    
    if as_html:
        return f"{html_link}"
    return f"{normal_link}"


def start_verification_event(email):
    email_obj, created = Email.objects.get_or_create(email=email)
    obj = EmailVerificationEvent.objects.create(
            parent= email_obj,
            email = email
        )
    sent = send_verification_email(obj.id)

    return obj, sent
# celery task -> background task
def send_verification_email(verify_obj_id):
    verify_obj = EmailVerificationEvent.objects.get(id = verify_obj_id )
    email =  verify_obj.email
    subject = 'Verifiy Your Email'
    text_msg = get_verification_email_msg(verify_obj, as_html= False)
    html_msg = get_verification_email_msg(verify_obj, as_html=True)
    from_user_email_address = EMAIL_HOST_USER
    to_user_email = email

    return send_mail(
        subject,
        text_msg,
        from_user_email_address,
        [to_user_email],
        fail_silently= False,
        html_message= html_msg
    )

   
   
def verfiy_token(token, max_attempts = 5):
    qs = EmailVerificationEvent.objects.filter(token=token)

    if not qs.exists() and not qs.count() == 1:
        return False, "invalid token", None
    
    """ has token """

    has_email_expired = qs.filter(expired = True)

    if has_email_expired:
        """ Token expired """
        return False, "Token expired, try again!", None
    
    """
    has not expired
    """

    max_attemps_reached = qs.filter(attemps__gte = max_attempts)
    if max_attemps_reached.exists():

        """update max attempts to +1"""
        #max_attemps_reached.update()

        return False, "token expired, used so many times", None
    
    """Token is valid"""

    """ update attemps, expire token if attemps > max """

    obj = qs.first()
    obj.attemps += 1
    obj.last_attemp_at = timezone.now()
    if obj.attemps > max_attempts:
        """ invalidation process """
        obj.expired = True
        obj.expired_at = timezone.now()
    obj.save()

    email_obj = obj.parent # Email.objects.get()
    
    return True, "Welcome", email_obj