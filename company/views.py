from tools.generic_views import *
from company.models import Company
from django.utils.translation import gettext as _
from django.db import transaction
from company.forms import CompanyCreateForm, CompanyForm, CompanyAdminForm, CompanyIbanFormSet
from tools.bce import get_data_from_bce
from django.contrib import messages
from django.urls import reverse


class CompanyCreateView(GenericCreateView):
    model = Company
    fields = None
    form_class = CompanyCreateForm
    success_message = _('Entreprise ajoutée.')
    
    def form_valid(self, form):
        c = form.save(commit=False)
        c.fill_data(get_data_from_bce(c.enterprise_number[2:]))
        c.save()
        self.request.user.companies.add(c)
        return super(CompanyCreateView, self).form_valid(form)


class CompanyListView(GenericListView):
    model = Company
    template_name = 'list_company.html'

    def get_queryset(self):
        queryset = self.request.user.companies.all().order_by('id')
        empty_fields = self.request.user.get_empty_fields()
        if empty_fields:
            if len(empty_fields) == 1:
                fields = empty_fields[0]
            else:
                fields = ", ".join(str(v) for v in empty_fields[:-1]) + " %s %s" % (_('and'), str(empty_fields[-1]))
            msg = '%s %s %s <a href=%s>%s</a>' % (_('Pour compléter votre profil, veuillez renseigner'), fields, _("cliquez"), reverse('customuser:profile_update'), _("ici"))
            messages.info(self.request, msg, extra_tags='safe')
            if self.request.user.schedule_meeting:
                #msg_calendar = "%s <a href=%s>%s</a>" % (_("Prenez un rendez-vous dès maintenant avec un membre de notre équipe cliquez"), reverse('agenda:slot_list'), _("ici"))
                msg_calendar = _("<b>Un expert comptable vous contactera pour prendre rendez-vous !</b>")
                messages.info(self.request, msg_calendar, extra_tags='safe')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': _("Mon entreprise")})
        context.update({'detail': _("Bienvenue sur votre compte LG & Associates. Depuis cette interface vous pouvez renseigner les informations de votre entreprise et gérer vos rendez-vous. Notre équipe est à votre disposition, prenez un rendez-vous dès maintenant pour commencer votre aventure au sein de notre cabinet. Nous nous adaptons à vos besoins en vous proposant des rendez-vous physiques ou en visioconférences.")})
        context.update({'add_label': _("Ajouter une entreprise")})

        return context


class CompanyUpdateView(GenericUpdateView):
    model = Company
    fields = None
    form_class = None
    template_name = 'update_company.html'


    def __init__(self, *args, **kwargs):
        super(CompanyUpdateView, self).__init__(*args, **kwargs)

    def get_form_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return CompanyAdminForm
        else:
            return CompanyForm

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        context.update({'title': _("Mon entreprise")})
        context.update({'detail': _("Les données ci-dessous proviennent de la Banque Carrefour des Entreprises.")})
        context.update({'add_iban' : _("Ajouter un iban")})
        context.update({'delete_iban' : _("supprimer")})
        self.form_class = CompanyForm
        if self.request.POST:
            context['ibans'] = CompanyIbanFormSet(self.request.POST, instance=self.object)
        else:
            context['ibans'] = CompanyIbanFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ibans = context['ibans']
        with transaction.atomic():
            # self.object = form.save()
            inst = form.save()
            if ibans.is_valid():
                # ibans.instance = self.object
                ibans.instance = inst
                ibans.save()
        return super(CompanyUpdateView, self).form_valid(form)


class CompanyDetailView(GenericDetailView):
    model = Company


class CompanyDeleteView(GenericDeleteView):
    model = Company
