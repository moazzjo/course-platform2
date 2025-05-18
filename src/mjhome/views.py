from django.shortcuts import render

from emails.models import Email, EmailVerificationEvent
from emails import services as email_services
from emails.forms import EmailForm
from django.conf import settings



def login_logout_view(request):
    return render(request,"auth/login-logout.html", {})

EMAIL_ADRESS = settings.EMAIL_ADRESS
def home_view(request, *args, **kwargs):
    template_name = 'home.html'
    print(request.POST)
    form = EmailForm(request.POST or None)
    context = {
        'form': form,
        'message': ''
    }

    if form.is_valid():
        email_val = form.cleaned_data.get("email")
        obj = email_services.start_verification_event(email_val)
        # obj = form.save()
        print(obj)
        context['form'] = EmailForm()
        context['message'] = f"Success! Check your email for verification from {EMAIL_ADRESS}"
    else:
        print(form.errors)

    print('email ID: ', request.session.get('email_id'))
    
    return render(request, template_name, context)
