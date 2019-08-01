from tools.generic_views import *
from company.models import Company
from django.utils.translation import gettext as _
from django.db import transaction
from company.forms import CompanyCreateForm, CompanyIbanFormSet
from tools.bce import get_data_from_bce
from django.contrib import messages
from django.urls import reverse


class CompanyCreateView(GenericCreateView):
    model = Company
    fields = None
    form_class = CompanyCreateForm

    def form_valid(self, form):
        c = form.save(commit=False)
        data = get_data_from_bce(c.enterprise_number[2:])
        if len(data):
            for key, value in data.items():
                if key == 'statut':
                    c.enterprise_status = value
                elif key == 'situation_juridique':
                    c.legal_situation = value
                elif key == 'date_debut':
                    c.start_date = value
                elif key == 'denomination':
                    c.enterprise_name = value
                elif key == 'adresse':
                    c.social_address_street = value
                elif key == 'adresse_num':
                    c.social_address_number = value
                elif key == 'adresse_cp':
                    c.social_address_zip = value
                elif key == 'adresse_ville':
                    c.social_address_city = value
                elif key == 'forme_legale':
                    c.legal_form = value
                elif key == 'date_fin_annee_comptable':
                    c.end_fiscal_date = value
        c.save()
        self.request.user.companies.add(c)
        return super(CompanyCreateView, self).form_valid(form)


class CompanyListView(GenericListView):
    model = Company

    def get_queryset(self):
        queryset = self.request.user.companies.all().order_by('id')
        if not self.request.user.telephone and not self.request.user.id_card:
            messages.info(self.request, 'Please fill in your phonenumber and a copy of your ID card. See <a href=%s>here</a>' % reverse('update_user'), extra_tags='safe')
        elif not self.request.user.telephone:
            messages.info(self.request, 'Please fill in your phonenumber. See <a href=%s>here</a>' % reverse('update_user'), extra_tags='html_safe')
        elif not self.request.user.id_card:
            messages.info(self.request, 'Please fill in a copy of your ID card. See <a href=%s>here</a>' % reverse('update_user'), extra_tags='safe')
        else:
            messages.success(self.request, "OK")
        return queryset


class CompanyUpdateView(GenericUpdateView):
    model = Company
    fields = '__all__'
    template_name = 'update_company.html'

    def get_context_data(self, **kwargs):
        data = super(CompanyUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['ibans'] = CompanyIbanFormSet(self.request.POST, instance=self.object)
        else:
            data['ibans'] = CompanyIbanFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ibans = context['ibans']
        with transaction.atomic():
            self.object = form.save()

            if ibans.is_valid():
                ibans.instance = self.object
                ibans.save()
        return super(CompanyUpdateView, self).form_valid(form)


class CompanyDetailView(GenericDetailView):
    model = Company


class CompanyDeleteView(GenericDeleteView):
    model = Company
