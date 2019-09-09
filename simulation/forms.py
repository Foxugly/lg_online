from django.forms import ModelForm
from .models import Simulation


class SimulationForm(ModelForm):
	class Meta:
		model = Simulation
		fields = ['nb_invoice']
