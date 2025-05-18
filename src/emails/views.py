from django.http import HttpResponse 
from django.contrib import messages
from django.conf import settings
from django_htmx.http import HttpResponseClientRedirect

from django.shortcuts import render, redirect

from . import services
# Create your views here.
from .forms import EmailForm
EMAIL_ADRESS = settings.EMAIL_ADRESS


def logout_btn_hx_view(request):
    if not request.htmx:
        redirect("/")

    if request.method == "POST":
        try:
            del request.session["email_id"]
        except:
            pass
        email_id_in_session = request.session.get("email_id")
        if not email_id_in_session:
            return HttpResponseClientRedirect('/')

    return render(request, "emails/hx/logout-btn.html", {})


def email_token_login_view(request):
    if not request.htmx:
        return redirect('/')
    email_id_in_session = request.session.get("email_id")
    template_name = "emails/hx/form.html"
    form = EmailForm(request.POST or None)
    context = {
        'form': form,
        'message': ' ',
        'show_form': not email_id_in_session

    }

    if form.is_valid():
        email_val = form.cleaned_data.get("email")
        obj = services.start_verification_event(email_val)
        # obj = form.save()
        print(obj)
        context['form'] = EmailForm()
        context['message'] = f"Success! Check your email for verification from {EMAIL_ADRESS}"
    else:
        print(form.errors)

    print('email ID: ', request.session.get('email_id'))
    
    return render(request, template_name, context)


def verfiy_email_token_view(request, token, *args, **kwargs):

    did_verfiy, msg, email_obj = services.verfiy_token(token)

    if not did_verfiy:
        try:
            del request.session["email_id"]

        except:
            pass
        messages.error(request, msg)
        return redirect("/login/")
    

    messages.success(request, msg)
    # Django -> request.session.get("email_id") 
    request.session["email_id"] = f"{email_obj.id}"

    next_url = request.session.get("next_url") or '/'
    if not next_url.startswith('/'):
        next_url = '/'

    return redirect(next_url)
