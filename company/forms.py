from django.forms import ModelForm
from company.models import Company
from localflavor.generic.forms import IBANFormField


class CompanyCreateForm(ModelForm):
    model = Company
    iban = IBANFormField()

    class Meta:
        model = Company
        fields = ['enterprise_number', 'iban']
        help_texts = {'enterprise_number': "ex 'BE0123456789",}


class CompanyUpdateForm(ModelForm):
    model = Company
    def __init__(self, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            #self.fields['enterprise_number_0'].widget.attrs['readonly'] = True
            self.fields['enterprise_number'].widget.attrs['readonly'] = True
            #self.fields['enterprise_number'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Company
        fields = ['enterprise_number', 'enterprise_status' ,'legal_situation', 'start_date', 'enterprise_name', 'social_address_street', 'social_address_number', 'social_address_zip', 'social_address_city', 'social_address_country', 'legal_form', 'end_fiscal_date', 'iban']