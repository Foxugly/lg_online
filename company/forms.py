from django.forms import ModelForm
from company.models import Company, Iban
from django.forms import inlineformset_factory


class CompanyCreateForm(ModelForm):
    model = Company

    class Meta:
        model = Company
        fields = ['enterprise_number', ]
        help_texts = {'enterprise_number': "ex 'BE0123456789", }



class CompanyAdminForm(ModelForm):
    model = Company

    def __init__(self, *args, **kwargs):
        super(CompanyAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['enterprise_number'].widget.attrs['readonly'] = True


    class Meta:
        model = Company
        fields = ['enterprise_number', 'enterprise_status', 'legal_situation',
                  'start_date', 'enterprise_name', 'social_address_street',
                  'social_address_number', 'social_address_zip',
                  'social_address_city', 'social_address_country',
                  'legal_form', 'end_fiscal_date', 'accountant', ]


class CompanyForm(ModelForm):
    model = Company

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['enterprise_number'].widget.attrs['readonly'] = True
        self.fields['start_date'].widget.attrs['class'] = 'date'



    class Meta:
        model = Company
        fields = ['enterprise_number', 'enterprise_status', 'legal_situation',
                  'start_date', 'enterprise_name', 'social_address_street',
                  'social_address_number', 'social_address_zip',
                  'social_address_city', 'social_address_country',
                  'legal_form', 'end_fiscal_date', ]


class CompanyProposalForm(ModelForm):
    model = Company

    class Meta:
        model = Company
        fields = ['calculated_amount', 'date_calculated_amount', 'proposed_amount' ]


class IbanUpdateForm(ModelForm):
    class Meta:
        model = Iban
        exclude = ()


CompanyIbanFormSet = inlineformset_factory(Company, Iban, form=IbanUpdateForm, extra=1,)
