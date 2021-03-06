import json

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin

from simulation.models import Simulation
from tools.mail import send_mail_smtp


class SimulationCreateView(CreateView):
    model = Simulation
    fields = ("turnover", "transmission", "nb_invoices_sale", "nb_invoices_purchase", "nb_managers", "nb_employees",
              "nb_creditcard", "alternatif_payments", "sector", "tax_liability")
    template_name = 'update_simulation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': _("Ma simulation personnalisée")})
        context.update({'detail': _(
            "Essayez de renseigner chaque indicateur avec des chiffres au plus près de votre activité pour avoir une estimation la plus fidèle possible.")})
        # TODO verbose_name
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
        context['price_calculated'] = self.object.calculated_amount
        context.update({'title': _("Ma simulation")})
        return context


def send_simulation_by_mail(request):
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
            subject = "[LG & Associates] " + _('Ma simulation personnalisée')
            s = Simulation.objects.get(pk=pk)
            url_simulation = "www.mylieutenantguillaume.com%s" % s.get_absolute_url()
            url_register = "www.mylieutenantguillaume.com%s?simulation_id=%d" % (
            reverse_lazy('customuser:customuser_add'), s.pk)

            msg_html = render_to_string('mail/simulation_email.html', {
                'url_simulation': url_simulation,
                'url_register': url_register
            })
            msg_txt = render_to_string('mail/simulation_email.txt', {
                'url_simulation': url_simulation,
                'url_register': url_register
            })
            send_mail_smtp(subject, email, None, msg_txt, msg_html, None)
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))
