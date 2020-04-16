from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from customuser.models import CustomUser
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib import messages
from customuser.forms import CustomUserCreateForm, CustomUserForm, MyPasswordResetForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from customuser.tokens import account_activation_token
from django.contrib.auth.forms import AuthenticationForm
from accountant.models import Accountant
from simulation.models import Simulation
from tools.generic_views import *
from django.contrib.messages.views import SuccessMessageMixin
from simulation.forms import SimulationAjustedForm, ReadOnlySimulationMixin
from django.contrib.auth.tokens import default_token_generator


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.accountant = Accountant.objects.filter(default=True)[0]
        user.save()
        messages.success(request, _('Thank you for your email confirmation. Now you can login your account.'))
        return redirect('home')
    else:
        messages.error(request, _('Activation link is invalid!'))
        return redirect('home')


def confirm_proposal(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        # TODO
        # si on a les data, il faut lancer l'install dans Fid et Yuki (méthode dans customuser lié à une company

        messages.success(request, _('Thank you for accepting our proposal ! You will receive in a few hours an email with all informations you will need !'))
        return redirect('home')
    else:
        messages.error(request, _('Activation link is invalid!'))
        return redirect('home')


class CustomUserLoginView(LoginView):
    model = CustomUser
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        if self.request.user.is_active:
            if self.request.user.is_staff or self.request.user.is_superuser:
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
        context.update({'title': _("Je m’enregistre")})
        context.update({'detail': _("Remplissez les champs suivants et n’oubliez pas de cliquer sur le lien de l’e-mail qui vous sera envoyé pour activer votre compte.")})
        # TODO verbose_name
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    fields = None
    form_class = CustomUserForm
    template_name = 'update.html'
    success_url = reverse_lazy('customuser:profile_update')
    success_message = _('Changes saved.')

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context.update({'title': _("Mise à jour de mon profil")})
        return context


class CustomUserUpdateView(GenericUpdateView):
    model = CustomUser
    fields = None
    form_class = CustomUserForm
    template_name = 'update.html'
    success_url = reverse_lazy('update_user')
    success_message = _('Changes saved.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context.update({'title': _("Mise à jour de mon profil")})
        return context


class MyPasswordResetView(PasswordResetView):
    model = CustomUser

    def __init__(self, *args, **kwargs):
        self.form_class = MyPasswordResetForm
        super(MyPasswordResetView, self).__init__(*args, **kwargs)


class CustomUserListView(GenericListView):
    model = CustomUser

    def get_queryset(self):
        return CustomUser.objects.filter(is_active=True, is_superuser=False)


class CustomUserDetailView(ReadOnlySimulationMixin, GenericUpdateView):
    model = CustomUser
    template_name = 'detail_customuser.html'
    fields = None
    form_class = SimulationAjustedForm

    def get_success_url(self):
        return reverse('customuser_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(CustomUserDetailView, self).get_context_data(**kwargs)
        context['form'] = SimulationAjustedForm(instance=self.object.simulation)
        return context

    def form_valid(self, form):
        instance = self.object.simulation
        instance.proposed_amount = form.cleaned_data.get('proposed_amount')
        instance.save()
        self.object.send_adjusted_proposition(self.object)
        return super(CustomUserDetailView, self).form_valid(form)


class CustomUserDeleteView(GenericDeleteView):
    model = CustomUser
