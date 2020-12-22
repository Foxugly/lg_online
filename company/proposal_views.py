import datetime

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, reverse
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from wkhtmltopdf.views import PDFTemplateResponse
from company.forms import CompanyProposalForm, CompanyPdfForm
from company.models import Company
from config_process import *
from customuser.forms import CustomUserPdfForm
from customuser.models import CustomUser
from simulation.forms import SimulationReadonlyForm, SimulationPdfForm
from tools.generic_views import *
from tools.mail import send_mail_smtp
from company.cron import my_scheduled_test


def get_users(c):
    return CustomUser.objects.filter(companies__id=c.pk)


def run_cron(request, pk):
    my_scheduled_test()
    context = {'title': _('Run cron'), 'text': _('scripts executed.'), }
    return render(request, "comment.html", context)


def run_config(request, pk):
    c = Company.objects.get(pk=pk)
    c.subscription_status = '6'
    c.save()
    user = get_users(c)[0]
    # TODO yuki and fid
    dict_context = {'company': c, 'user': user, 'domain': domain}
    msg_html = render_to_string('mail/step7_send_credentials.html', dict_context)
    msg_txt = render_to_string('mail/step7_send_credentials.txt', dict_context)
    subject = '%s %s' % (tag, subject_step7)
    send_mail_smtp(subject, user.email, reply_to, msg_txt, msg_html, None)
    if show_msg:
        print(msg_txt)
    context = {'title': _('Create companies in softwares'), 'text': _('Procedure started.'), }
    return render(request, "comment.html", context)


def send_proposal(request, pk):
    c = Company.objects.get(pk=pk)
    c.token = get_random_string(length=64)
    c.subscription_status = '4'
    c.save()
    for user in get_users(c):
        if not c.date_proposed_amount:
            c.date_proposed_amount = datetime.datetime.today()
            c.save()
        subject = '%s %s' % (tag, subject_step5)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token_company = c.token
        token = default_token_generator.make_token(user)

        dict_context = {'company': c, 'user': user, 'domain': domain, 'uid': uid,
                        'token_company': token_company, 'token': token, }
        msg_html = render_to_string('mail/step5_send_final_proposal.html', dict_context)
        msg_txt = render_to_string('mail/step5_send_final_proposal.txt', dict_context)
        reply_to = "info@lieutenantguillaume.com"
        #if show_msg:
        #    print(msg_txt)
        send_mail_smtp(subject, user.email, reply_to, msg_txt, msg_html, None)
    context = {'title': _('Offre finale envoyée'), 'text': _('La proposition finale a été envoyée.'), }
    return render(request, "comment.html", context)


def confirm_proposal(request, pk, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    context = {'title': _('Offre finale acceptée')}
    if user is not None and default_token_generator.check_token(user, token):
        c = Company.objects.get(pk=pk)
        c.subscription_status = '5'
        c.save()
        dict_context = {'company': c, 'user': user, 'domain': domain, 'token_company': c.token}
        msg_html = render_to_string('mail/step6_final_proposal_accepted.html', dict_context)
        msg_txt = render_to_string('mail/step6_final_proposal_accepted.txt', dict_context)
        subject = '%s %s' % (tag, subject_step6)
        send_mail_smtp(subject, user.email, reply_to, msg_txt, msg_html, None)
        send_mail_smtp(subject, c.accountant.email, reply_to, msg_txt, msg_html, None)
        if show_msg:
            print(msg_txt)
        context['text'] = _(
            " Merci d'avoir accepté notre proposition. Nous vous contacterons rapidement pour vous communiquer vos accès")
    else:
        context['text'] = _("Une erreur est survenue avec le lien")
    return render(request, "comment.html", context)


class CompanyProposalListView(GenericListView):
    model = Company
    template_name = 'list_company_proposal.html'

    def get_queryset(self):
        return [(c, get_users(c)) for c in Company.objects.all()]


class CompanyProposalUpdateView(GenericUpdateView):
    model = Company
    fields = None
    form_class = CompanyProposalForm
    template_name = 'update_proposal.html'

    def __init__(self, *args, **kwargs):
        super(CompanyProposalUpdateView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'SimulationForm': SimulationReadonlyForm(instance=self.object.simulation)})
        return context

    def get_success_url(self):
        return reverse('company:company_proposal_list')


class CompanyProposalPdfView(DetailView):
    model = Company
    template_name = 'pdf/company_proposal_raw.html'
    context = {}

    def get(self, request, pk, token):
        c = self.get_object()
        if c.token == token:
            self.context['object'] = c
            self.context['companyForm'] = CompanyPdfForm(instance=c)
            self.context['simulationForm'] = SimulationPdfForm(instance=c.simulation)
            self.context['clientForm'] = CustomUserPdfForm(instance=get_users(c)[0])
            name = '%s%05d' % (c.date_proposed_amount.strftime("%Y%m%d%H%M%s"), c.pk)
            filename = '%s_proposal.pdf' % name
            self.context['name'] = name
            response = PDFTemplateResponse(request=request,
                                           template=self.template_name,
                                           filename=filename,
                                           context=self.context,
                                           show_content_in_browser=True,
                                           cmd_options={'margin-top': 50, },
                                           )
            return response
        else:
            context = {'title': _('Confirm proposal'), 'text': _('Le lien est incorrect.'), }
            return render(request, "comment.html", context)
