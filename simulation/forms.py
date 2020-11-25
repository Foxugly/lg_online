from django.forms import ModelForm
from django.views.generic.edit import ModelFormMixin

from .models import Simulation


class SimulationForm(ModelForm):
    class Meta:
        model = Simulation
        fields = "__all__"


class SimulationAjustedForm(ModelForm):
    class Meta:
        model = Simulation
        fields = "__all__"


class ReadOnlySimulationMixin(ModelFormMixin):

    def get_form(self, form_class=None):
        form = super(ReadOnlySimulationMixin, self).get_form()
        for field in form.fields:
            form.fields[field].widget.attrs['readonly'] = 'readonly'
            form.fields[field].widget.attrs['disabled'] = 'disabled'
        return form

    def form_valid(self, form):
        return self.form_invalid(form)


class SimulationReadonlyForm(ReadOnlySimulationMixin, ModelForm):
    class Meta:
        model = Simulation
        fields = "__all__"
        exclude = ('calculated_amount', 'date_calculated_amount')


class SimulationPdfForm(ModelForm):
    model = Simulation

    def is_valid(self):
        return False

    class Meta:
        model = Simulation
        fields = ['turnover', 'transmission', 'nb_invoices_sale', 'nb_invoices_purchase', 'nb_managers', 'nb_employees',
                  'nb_creditcard', 'alternatif_payments', 'sector', 'tax_liability', ]
