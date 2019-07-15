from django.shortcuts import render, redirect
from customuser.models import CustomUser
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from .models import CustomUser
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib import messages
from .forms import CustomUserCreateForm, CustomUserForm, CustomUserDataForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from tools.bce import get_data_from_bce


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        data = get_data_from_bce(user.enterprise_number)
        if len(data):
            for key, value in data.items():
                if key =='statut': 
                    user.enterprise_status = value
                elif key == 'situation_juridique':
                    user.legal_situation = value
                elif key == 'date_debut': 
                    user.start_date = value
                elif key == 'denomination': 
                    user.enterprise_name = value
                elif key == 'adresse': 
                    user.social_address_street = value
                elif key == 'adresse_num': 
                    user.social_address_number = value
                elif key == 'adresse_cp': 
                    user.social_address_zip = value
                elif key == 'adresse_ville': 
                    user.social_address_city = value
                elif key == 'forme_legale': 
                    user.legal_form = value
                elif key == 'date_fin_annee_comptable':
                    user.end_fiscal_date = value
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('home')
        #return render(request, "index.html")
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')
        #return render(request, "index.html")


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
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)


class CustomUserUpdateView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('update_user')
    success_message = _('Changes saved.')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        return context


class CustomUserUpdataDataView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserDataForm
    template_name = 'update.html'
    success_url = reverse_lazy('customuser:update_data')
    success_message = _('Changes saved.')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        return context