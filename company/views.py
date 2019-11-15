from tools.generic_views import *
from company.models import Company
from django.utils.translation import gettext as _
from django.db import transaction
from company.forms import CompanyCreateForm, CompanyForm, CompanyIbanFormSet
from tools.bce import get_data_from_bce
from django.contrib import messages
from django.urls import reverse


class CompanyCreateView(GenericCreateView):
    model = Company
    fields = None
    form_class = CompanyCreateForm

    def form_valid(self, form):
        c = form.save(commit=False)
        c.fill_data(get_data_from_bce(c.enterprise_number[2:]))
        c.save()
        self.request.user.companies.add(c)
        return super(CompanyCreateView, self).form_valid(form)


class CompanyListView(GenericListView):
    model = Company

    def get_queryset(self):
        queryset = self.request.user.companies.all().order_by('id')
        empty_fields = self.request.user.get_empty_fields()
        if empty_fields:
            if len(empty_fields) == 1:
                fields = empty_fields[0]
            else:
                fields = ", ".join(str(v) for v in empty_fields[:-1]) + " %s %s" % (_('and'), str(empty_fields[-1]))
            messages.info(self.request, 'Please fill in %s. See <a href=%s>here</a>' % (fields, reverse('customuser:profile_update')),
                          extra_tags='safe')

        return queryset


class CompanyUpdateView(GenericUpdateView):
    model = Company
    fields = None
    form_class = CompanyForm
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
