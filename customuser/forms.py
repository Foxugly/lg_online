from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.forms import ModelForm
from django.template import loader
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from vies.validators import VATINValidator

from config_process import *
from customuser.models import CustomUser
from customuser.tokens import account_activation_token
from tools.mail import send_mail_smtp


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
        self.fields['address_country'].widget.attrs['data-live-search'] = 'true'
        self.fields['id_card'].widget.attrs['class'] = "form-control"

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'telephone', 'address_street', 'address_number', 'address_zip',
                  'address_city', 'address_country', 'id_card', 'language']


class CustomUserCreateForm(UserCreationForm):
    model = CustomUser
    enterprise_number = forms.CharField(label=_("Enterprise Number"), required=True,
                                        help_text=_("ex 'BE0123456789' pas de points, pas d'espaces"),
                                        validators=[VATINValidator(verify=True)])
    captcha = CaptchaField(label=_('Captcha'), error_messages=dict(invalid="%s" % (_("Invalid CAPTCHA"))))

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'language', ]
        help_texts = {'enterprise_number': "ex 'BE0123456789'", }

    def is_valid(self):
        valid = super(CustomUserCreateForm, self).is_valid()
        if not valid:
            return valid
        user = self.save(commit=False)
        user.is_active = False
        user.save()
        subject = '%s %s' % (tag, subject_step1)
        dict_context = {'user': user, 'domain': domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user), }
        msg_html = render_to_string('mail/step1_subscribe.html', dict_context)
        msg_txt = render_to_string('mail/step1_subscribe.txt', dict_context)
        to = self.cleaned_data.get('email')
        send_mail_smtp(str(subject), to, reply_to, msg_txt, msg_html, None)
        if show_msg:
            print(msg_txt)
        return valid


class MyPasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = '[%s] ' % domain + loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        send_mail_smtp(str(subject), to_email, None, body, None, None)


class CustomUserPdfForm(ModelForm):
    model = CustomUser

    def is_valid(self):
        return False

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'telephone', 'email', 'address_street', 'address_number', 'address_zip',
                  'address_city', 'address_country', 'language']
