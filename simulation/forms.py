from django.forms import ModelForm
from .models import Simulation
from django.views.generic.edit import ModelFormMixin


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
            if field != "proposed_amount":
                form.fields[field].widget.attrs['readonly'] = 'readonly'
                form.fields[field].widget.attrs['disabled'] = 'disabled'
        return form

    def form_valid(self, form):
        return self.form_invalid(form)
