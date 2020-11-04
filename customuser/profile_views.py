
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from accountant.models import Accountant
from customuser.forms import CustomUserForm
from customuser.models import CustomUser
from customuser.tokens import account_activation_token
from tools.generic_views import *


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
        user.save()
        c['text'] = _('Thank you for your email confirmation. Now you can login your account.')
    else:
        c['text'] = _('Activation link is invalid!')
    # TODO send email to accountant to book meeting
    print("TODO send email to accountant to book meeting")
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
