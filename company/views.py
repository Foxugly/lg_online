from tools.generic_views import *
from company.models import Company
from django.utils.translation import gettext as _
from django.db import transaction
from company.forms import CompanyCreateForm, CompanyForm, CompanyAdminForm, CompanyIbanFormSet, CompanyProposalForm
from simulation.forms import SimulationReadonlyForm, SimulationPdfForm
from tools.bce import get_data_from_bce
from django.contrib import messages
from django.urls import reverse
from customuser.models import CustomUser
from customuser.forms import CustomUserPdfForm
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from wkhtmltopdf.views import PDFTemplateResponse
import datetime
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from tools.mail import send_mail_smtp
from company.forms import CompanyPdfForm


def get_users(c):
    return CustomUser.objects.filter(companies__id=c.pk)


def send_proposal(request, pk):
    c = Company.objects.get(pk=pk)
    for user in get_users(c):
        print(user)
        subject = _('[LG&Associates] Final proposal')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token_company = default_token_generator.make_token(c)
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


def confirm_proposal(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        print("TODO Lancer l'install dans FID et YUKI")
        # si on a les data, il faut lancer l'install dans Fid et Yuki (méthode dans customuser lié à une company
        # TODO
        messages.success(request, _(
            'Thank you for accepting our proposal ! You will receive in a few hours an email with all informations you will need !'))
        return redirect('home')
    else:
        messages.error(request, _('Activation link is invalid!'))
        return redirect('home')


class CompanyCreateView(GenericCreateView):
    model = Company
    fields = None
    form_class = CompanyCreateForm
    success_message = _('Entreprise ajoutée.')
    
    def form_valid(self, form):
        c = form.save(commit=False)
        c.fill_data(get_data_from_bce(c.enterprise_number[2:]))
        c.save()
        self.request.user.companies.add(c)
        return super(CompanyCreateView, self).form_valid(form)


class CompanyProposalListView(GenericListView):
    model = Company
    template_name = 'list_company_proposal.html'

    def get_queryset(self):
        return [(c, get_users(c)) for c in Company.objects.all()]


class CompanyListView(GenericListView):
    model = Company
    template_name = 'list_company.html'

    def get_queryset(self):
        queryset = self.request.user.companies.all().order_by('id')
        empty_fields = self.request.user.get_empty_fields()
        if empty_fields:
            if len(empty_fields) == 1:
                fields = empty_fields[0]
            else:
                fields = ", ".join(str(v) for v in empty_fields[:-1]) + " %s %s" % (_('and'), str(empty_fields[-1]))
            msg = '%s %s %s <a href=%s>%s</a>' % (_('Pour compléter votre profil, veuillez renseigner'), fields, _("cliquez"), reverse('customuser:profile_update'), _("ici"))
            messages.info(self.request, msg, extra_tags='safe')
            if self.request.user.schedule_meeting:
                #msg_calendar = "%s <a href=%s>%s</a>" % (_("Prenez un rendez-vous dès maintenant avec un membre de notre équipe cliquez"), reverse('agenda:slot_list'), _("ici"))
                msg_calendar = _("<b>Un expert comptable vous contactera pour prendre rendez-vous !</b>")
                messages.info(self.request, msg_calendar, extra_tags='safe')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': _("Mon entreprise")})
        context.update({'detail': _("Bienvenue sur votre compte LG & Associates. Depuis cette interface vous pouvez renseigner les informations de votre entreprise et gérer vos rendez-vous. Notre équipe est à votre disposition, prenez un rendez-vous dès maintenant pour commencer votre aventure au sein de notre cabinet. Nous nous adaptons à vos besoins en vous proposant des rendez-vous physiques ou en visioconférences.")})
        context.update({'add_label': _("Ajouter une entreprise")})
        return context


class CompanyUpdateView(GenericUpdateView):
    model = Company
    fields = None
    form_class = None
    template_name = 'update_company.html'


    def __init__(self, *args, **kwargs):
        super(CompanyUpdateView, self).__init__(*args, **kwargs)

    def get_form_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return CompanyAdminForm
        else:
            return CompanyForm

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        context.update({'title': _("Mon entreprise")})
        context.update({'detail': _("Les données ci-dessous proviennent de la Banque Carrefour des Entreprises.")})
        context.update({'add_iban' : _("Ajouter un iban")})
        context.update({'delete_iban': _("supprimer")})
        self.form_class = CompanyForm
        if self.request.POST:
            context['ibans'] = CompanyIbanFormSet(self.request.POST, instance=self.object)
        else:
            context['ibans'] = CompanyIbanFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ibans = context['ibans']
        with transaction.atomic():
            # self.object = form.save()
            inst = form.save()
            if ibans.is_valid:
                # ibans.instance = self.object
                ibans.instance = inst
                ibans.save()
        inst = form.save()
        if inst.get_empty_fields() == None:
            print("FULL")
        return super(CompanyUpdateView, self).form_valid(form)


class CompanyDetailView(GenericDetailView):
    model = Company


class CompanyDeleteView(GenericDeleteView):
    model = Company


class CompanyProposalUpdateView(GenericUpdateView):
    model = Company
    fields = None
    form_class = CompanyProposalForm
    template_name = 'update_proposal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'SimulationForm': SimulationReadonlyForm(instance=self.object.simulation)})
        return context


class CompanyProposalPdfView(DetailView):
    model = Company
    template_name = 'company_proposal_raw.html'
    context = {}

    def get(self, request, pk, token):
        print(token)
        self.context['object'] = self.get_object()
        self.context['companyForm'] = CompanyPdfForm(instance=self.get_object())
        self.context['simulationForm'] = SimulationPdfForm(instance=self.get_object().simulation)
        self.context['clientForm'] = CustomUserPdfForm(instance=get_users(self.get_object())[0])
        name = '%s%05d' % (datetime.datetime.now().strftime("%Y%m%d%H%M%S"), self.get_object().pk)
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