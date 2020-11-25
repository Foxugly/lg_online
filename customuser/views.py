from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordResetView
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from company.models import Company
from customuser.forms import CustomUserCreateForm, CustomUserForm, MyPasswordResetForm
from customuser.models import CustomUser
from simulation.forms import SimulationAjustedForm, ReadOnlySimulationMixin
from simulation.models import Simulation
from tools.bce import get_data_from_bce
from tools.generic_views import *


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
    success_message = "Account created"

    def __init__(self, *args, **kwargs):
        if self.model:
            self.app_name = self.model._meta.app_label
            self.model_name = self.model._meta.model_name
        super(CustomUserCreateView, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        if self.request.GET.get('simulation_id'):
            instance = form.save(commit=False)
            instance.simulation = Simulation.objects.get(pk=self.request.GET.get('simulation_id'))

            c = Company(enterprise_number=form.cleaned_data.get('enterprise_number'), simulation=instance.simulation,
                        calculated_amount=instance.simulation.calculated_amount,
                        date_calculated_amount=instance.simulation.date_calculated_amount,
                        proposed_amount=instance.simulation.calculated_amount)
            c.fill_data(get_data_from_bce(form.cleaned_data.get('enterprise_number')[2:]))
            c.save()
            instance.companies.add(c)
            instance.save()
        return super(CustomUserCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CustomUserCreateView, self).get_context_data(**kwargs)
        context.update({'title': _("Je m’enregistre")})
        context.update({'detail': _(
            "Remplissez les champs suivants et n’oubliez pas de cliquer sur le lien de l’e-mail qui vous sera envoyé pour activer votre compte.")})
        # TODO verbose_name
        return context

    def get_success_url(self):
        return reverse("comment_creation")


class CustomUserUpdateView(GenericUpdateView):
    model = CustomUser
    fields = None
    form_class = CustomUserForm
    template_name = 'update.html'
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
    template_name = 'list.html'

    def get_queryset(self):
        return CustomUser.objects.filter(is_active=True, is_superuser=False)


class CustomUserDetailView(ReadOnlySimulationMixin, GenericUpdateView):
    model = CustomUser
    template_name = 'detail.html'
    fields = None
    form_class = SimulationAjustedForm

    def get_success_url(self):
        return reverse('customuser_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(CustomUserDetailView, self).get_context_data(**kwargs)
        context['form'] = SimulationAjustedForm(instance=self.object.simulation)
        return context


class CustomUserDeleteView(GenericDeleteView):
    model = CustomUser
