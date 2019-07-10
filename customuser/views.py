from django.shortcuts import render
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
from .forms import CustomUserCreateForm, CustomUserForm


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
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return render(request, "index.html")
    else:
        messages.error(request, 'Activation link is invalid!')
        return render(request, "index.html")


class CustomUserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreateForm
    template_name = 'update.html'
    success_url = reverse_lazy('home')
    success_message = _('We just send you an email for validation.')


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
