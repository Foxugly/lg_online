from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from customuser.models import CustomUser
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib import messages
from customuser.forms import CustomUserCreateForm, CustomUserForm, MyPasswordResetForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from customuser.tokens import account_activation_token
from django.contrib.auth.forms import AuthenticationForm
from contact.models import Contact
from simulation.models import Simulation
from tools.generic_views import *


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.contact = Contact.objects.filter(default=True)[0]
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')


class CustomUserLoginView(LoginView):
    model = CustomUser
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        if self.request.user.is_active:
            if self.request.user.is_staff or self.request.user.is_superuser :
                return reverse_lazy('customuser:customuser_list')
            else:
                return reverse_lazy('company:company_list')


class CustomUserCreateView(GenericCreateView):
    model = CustomUser
    fields = None
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

    def form_valid(self, form):
        if self.request.GET.get('simulation_id'):
            instance = form.save(commit=False)
            simulation_id = self.request.GET.get('simulation_id')
            instance.simulation = Simulation.objects.get(pk=simulation_id)
        return super(CustomUserCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CustomUserCreateView, self).get_context_data(**kwargs)
        context.update({'title': "New User"})
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)


class CustomUserUpdateView(GenericUpdateView):
    model = CustomUser
    fields = None
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


class MyPasswordResetView(PasswordResetView):
    model = CustomUser

    def __init__(self, *args, **kwargs):
        self.form_class = MyPasswordResetForm


class CustomUserListView(GenericListView):
    model = CustomUser

    def get_queryset(self):
       return CustomUser.objects.filter(is_active=False, is_superuser=False)


class CustomUserDetailView(GenericDetailView):
    model = CustomUser


class CustomUserDeleteView(GenericDeleteView):
    model = CustomUser
