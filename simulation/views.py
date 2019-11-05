
from .models import Simulation
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponse
import json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from tools.mail import send_mail_smtp
from django.views.generic.edit import ModelFormMixin


class SimulationCreateView(CreateView):
    model = Simulation
    fields = ("turnover", "transmission", "nb_invoices_sale", "nb_invoices_purchase", "nb_managers", "nb_employees",
              "nb_creditcard", "alternatif_payments", "sector", "tax_liability")
    template_name = 'update_simulation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': "Simulation"})
        return context

    def get_initial(self):
        super(SimulationCreateView, self).get_initial()
        if self.request.GET.get('simulation_id'):
            simulation = Simulation.objects.get(pk=self.request.GET.get('simulation_id'))
            self.initial = {
                'transmission': simulation.transmission,
                'turnover': simulation.turnover,
                'nb_invoices_sale': simulation.nb_invoices_sale,
                'nb_invoices_purchase': simulation.nb_invoices_purchase,
                'nb_managers': simulation.nb_managers,
                'nb_employees': simulation.nb_employees,
                'nb_creditcard': simulation.nb_creditcard,
                'alternatif_payments': simulation.alternatif_payments,
                'sector': simulation.sector,
                'tax_liability': simulation.tax_liability,
            }
        return self.initial


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
    fields = ("turnover", "transmission", "nb_invoices_sale", "nb_invoices_purchase", "nb_managers", "nb_employees",
              "nb_creditcard", "alternatif_payments", "sector", "tax_liability")
    template_name = 'update_simulation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        context['price'], context['price_calculated'] = self.object.compute()
        context.update({'title': "Simulation"})
        return context


def send_mail(mail, pk):
    subject = "[LG & Associates] devis"
    s = Simulation.objects.get(pk=pk)
    text = "Hello,\n\n"
    text += "Link to your devis : %s" % s.get_absolute_url()
    print(text)
    send_mail_smtp(subject, mail, None, text, None)


def send_simulation_by_mail(request):
    print("COMPUTE_SIMULATION")
    results = {}
    if request.is_ajax():
        pk = request.POST['pk']
        email = request.POST['email']
        try:
            validate_email(email)
            results['return'] = True
        except ValidationError:
            results['return'] = False
        if results['return']:
            send_mail(email, pk)
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))
