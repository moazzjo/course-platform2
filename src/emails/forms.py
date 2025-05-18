from django import forms

from . import css,services  
from .models import Email

class EmailForm(forms.Form):
    email = forms.EmailField(
        label ="",
        widget=forms.EmailInput(
            
            attrs={
                "id":"email-login-input",
                "class": css.Email_input_style,
                "placeholder": "Enter Your Email"
            }
        )
    )


    # class Meta:
    #     model = EmailVerificationEvent
    #     fields = ['email']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        verified = services.verify_email(email)

        if verified:
            raise forms.ValidationError("Invalid Email, Please try again")


        return email



    




