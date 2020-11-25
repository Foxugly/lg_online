from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from accountant.models import Accountant
from config_process import *
from customuser.forms import CustomUserForm
from customuser.models import CustomUser
from customuser.tokens import account_activation_token
from tools.generic_views import *
from tools.mail import send_mail_smtp


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    c = {'title': _('Activation'),
         'text': _('None')}
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.accountant = Accountant.objects.filter(default=True)[0]
        for comp in user.companies.all():
            if not comp.accountant:
                if comp.subscription_status == '1':
                    comp.subscription_status = '2'
                    comp.subscription_date = timezone.now() + time_to_complete_subscription
                    # send mail
                    dict_context = {'company': c, 'user': user, 'domain': domain, }
                    msg_html = render_to_string('mail/step2_account_actived.html', dict_context)
                    msg_txt = render_to_string('mail/step2_account_actived.txt', dict_context)
                    subject = '%s %s' % (tag, subject_step2)
                    send_mail_smtp(subject, user.email, reply_to, msg_txt, msg_html, None)
                    if show_msg:
                        print(msg_txt)
                comp.accountant = user.accountant
                comp.save()
        user.save()

        c['text'] = _('Thank you for your email confirmation. Now you can login your account.')
    else:
        c['text'] = _('Activation link is invalid!')
    # TODO send email to accountant to book meeting
    # dict_context = {'company': c, 'user': user, 'domain': domain, }
    # msg_html = render_to_string('mail/step2b_new_client.html', dict_context)
    # msg_txt = render_to_string('mail/step2b_new_client.txt', dict_context)
    # subject = '%s %s' % (tag, subject_step2)
    # send_mail_smtp(subject, user.accountant.email, reply_to, msg_txt, msg_html, None)
    return render(request, "comment.html", c)


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    fields = None
    form_class = CustomUserForm
    template_name = 'update.html'
    success_url = reverse_lazy('customuser:profile_update')
    success_message = _('Changes saved.')

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context.update({'title': _("Mise à jour de mon profil")})
        return context
