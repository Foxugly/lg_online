from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.forms import ModelForm
from customuser.models import CustomUser
from captcha.fields import CaptchaField
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from customuser.tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.translation import gettext_lazy as _
from django import forms
from tools.mail import send_mail_smtp
from django.contrib.auth import authenticate
from django.template import loader


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserForm(ModelForm):
    model = CustomUser

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'telephone', 'id_card', 'language']


class CustomUserCreateForm(UserCreationForm):
    model = CustomUser
    # password = forms.CharField(widget=forms.PasswordInput)
    # repeat_password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'language', ]

    def is_valid(self):
        valid = super(CustomUserCreateForm, self).is_valid()
        if not valid:
            return valid
        user = self.save(commit=False)
        user.is_active = False
        user.save()
        # current_site = Site.objects.get_current()
        subject = _('[mylieutenantguillaume] activation for your account')
        msg_html = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': 'www.mylieutenantguillaume.com',  # current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        msg_txt = render_to_string('acc_active_email.txt', {
            'user': user,
            'domain': 'www.mylieutenantguillaume.com',  # current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to = self.cleaned_data.get('email')
        reply_to = "info@lieutenantguillaume.com"
        send_mail_smtp(str(subject), to, reply_to, msg_txt, msg_html)
        return valid


class MyPasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = '[mylieutenantguillaume] ' + loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        send_mail_smtp(str(subject), to_email, None, body, None)

