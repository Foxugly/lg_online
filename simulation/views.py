from tools.generic_views import *
from .models import Simulation
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView
from .forms import SimulationForm
from django.http import HttpResponse
import json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from tools.mail import send_mail_smtp
from django.views.generic.edit import FormMixin, ModelFormMixin


class SimulationCreateView(CreateView):
    model = Simulation
    fields = "__all__"
    template_name = 'update_simulation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': "Simulation"})
        return context


class ReadOnlyModelFormMixin(ModelFormMixin):

    def get_form(self, form_class=None):
        form = super(ReadOnlyModelFormMixin, self).get_form()
        for field in form.fields:
            form.fields[field].widget.attrs['readonly'] = 'readonly'          
            form.fields[field].widget.attrs['disabled'] = 'disabled'
        return form

    def form_valid(self, form): 
        return self.form_invalid(form)


class SimulationUpdateView(UpdateView, ReadOnlyModelFormMixin):
    model = Simulation
    fields = '__all__'
    template_name = 'update_simulation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        context['price'], context['price_calculated'] = self.object.compute()
        context.update({'title': "Simulation"})
        return context



def send_mail(mail, pk):
    subjct = "[LG & Associates] devis"
    s = Simulation.objects.get(pk=pk)
    text = "Hello,\n\n"
    text += "Link to your devis : %s" % s.get_absolute_url()
    print(text)
    #send_mail_smtp(subject, mail, None, text, html)


def send_simulation_by_mail(request):
    print("COMPUTE_SIMULATION")
    results = {}
    if request.is_ajax():
        pk = request.POST['pk']
        email = request.POST['email']
        try:
            validate_email( email)
            results['return'] = True
        except ValidationError:
            results['return'] = False
        if results['return']:
            send_mail(email, pk)
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))