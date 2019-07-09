from django.shortcuts import render
from customuser.models import CustomUser
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login
from django.http import HttpResponse
from captcha.fields import CaptchaField


class CustomUserForm(ModelForm):
    model = CustomUser
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['is_foo_admin'].widget.attrs['readonly'] = True
            self.fields['is_foo_admin'].widget.attrs['disabled'] = 'disabled'
            self.fields['is_superuser'].widget.attrs['readonly'] = True
            self.fields['is_superuser'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'language', 'is_foo_admin', 'is_superuser', ]



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class CustomUserCreateForm(ModelForm):
    model = CustomUser
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'enterprise_number',
            'password',
        ]

    def is_valid(self):
        valid = super(CustomUserCreateForm, self).is_valid()
        if not valid:
            return valid
        user = self.save(commit=False)
        user.is_active = False
        user.save()
        # current_site = Site.objects.get_current()
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': '127.0.0.1:8000', # current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = self.cleaned_data.get('email')
        print(message)
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()


class CustomUserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreateForm
    app_name = None
    model_name = None
    template_name = 'update.html'
    success_url = 'index.html'
    success_message = _('object created.')


class CustomUserUpdateView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'update.html'
    success_url = reverse_lazy('update_user')
    success_message = _('Changes saved.')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        return context
