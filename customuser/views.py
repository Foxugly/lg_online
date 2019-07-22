from django.shortcuts import render, redirect
from customuser.models import CustomUser
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from customuser.models import CustomUser
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.contrib import messages
from customuser.forms import CustomUserCreateForm, CustomUserForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from customuser.tokens import account_activation_token
from django.contrib.auth.forms import AuthenticationForm


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('home')
        #return render(request, "index.html")
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')
        #return render(request, "index.html")


class CustomUserLoginView(LoginView):
    model = CustomUser
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('company:company_list')


class CustomUserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreateForm
    template_name = 'update.html'
    success_url = reverse_lazy('home')
    success_message = _('We just send you an email for validation.')

    def __init__(self, *args, **kwargs):
        if self.model:
            self.app_name = self.model._meta.app_label
            self.model_name = self.model._meta.model_name
            self.success_url = reverse_lazy('home')
        super(CustomUserCreateView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomUserCreateView, self).get_context_data(**kwargs)
        context.update({'title': "New User"})
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)


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
        context.update({'title': "Update User"})
        return context
