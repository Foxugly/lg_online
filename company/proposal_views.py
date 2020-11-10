import datetime
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from wkhtmltopdf.views import PDFTemplateResponse
from company.forms import CompanyProposalForm, CompanyPdfForm
from company.models import Company
from customuser.forms import CustomUserPdfForm
from customuser.models import CustomUser
from simulation.forms import SimulationReadonlyForm, SimulationPdfForm
from tools.generic_views import *
from tools.mail import send_mail_smtp
from django.utils.translation import gettext as _


def get_users(c):
    return CustomUser.objects.filter(companies__id=c.pk)


def run_config(request, pk):
    company = Company.objects.get(pk=pk)
    print("TODO run sync with yuki and fid")
    #TODO yuki and fid
    company.active = True
    company.save()
    context = {'title': _('Create companies in softwares'), 'text': _('Procedure started.'), }
    return render(request, "comment.html", context)


def send_proposal(request, pk):
    c = Company.objects.get(pk=pk)
    c.token = get_random_string(length=64)
    c.sent = True
    c.save()
    for user in get_users(c):
        if not c.date_proposed_amount:
            c.date_proposed_amount = datetime.datetime.today()
            c.save()
        subject = _('[LG&Associates] Final proposal')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token_company = c.token
        token = default_token_generator.make_token(user)

        context = {'company': c, 'user': user, 'domain': 'www.mylieutenantguillaume.com', 'uid': uid,
                   'token_company': token_company, 'token': token, }
        msg_html = render_to_string('acc_confirm_proposal.html', context)
        msg_txt = render_to_string('acc_confirm_proposal.txt', context)
        to = user.email
        reply_to = "info@lieutenantguillaume.com"
        print(msg_txt)
        # TODO create pdf with simulation
        send_mail_smtp(str(subject), to, reply_to, msg_txt, msg_html, None)
    context = {'title': _('Activation'), 'text': _('La proposition finale a été envoyée.'), }
    return render(request, "comment.html", context)


def confirm_proposal(request, pk, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        c = Company.objects.get(pk=pk)
        c.valid_user = True
        c.save()
        print("TODO Lancer l'install dans FID et YUKI")
        # si on a les data, il faut lancer l'install dans Fid et Yuki (méthode dans customuser lié à une company
        # TODO
        messages.success(request, _(
            'Thank you for accepting our proposal ! You will receive in a few hours an email with all informations you will need !'))
        return redirect('home')
    else:
        messages.error(request, _('Activation link is invalid!'))
        return redirect('home')


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


class CompanyProposalPdfView(DetailView):
    model = Company
    template_name = 'company_proposal_raw.html'
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
