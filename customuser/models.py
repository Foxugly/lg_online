from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from company.models import Company
from phonenumber_field.modelfields import PhoneNumberField
from simulation.models import Simulation
from tools.generic_class import GenericClass
from django.contrib.auth.tokens import default_token_generator 
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from tools.mail import send_mail_smtp
from django_countries.fields import CountryField


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password):
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, GenericClass):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    language = models.CharField(_("language"), max_length=8, choices=settings.LANGUAGES, default=1)
    companies = models.ManyToManyField(Company, blank=True, verbose_name=_("companies"))
    telephone = PhoneNumberField(_("Phone number"), max_length=20, blank=True)
    id_card = models.FileField(upload_to=settings.IDCARD_URL, blank=True)
    address_street = models.CharField(_("Street"), max_length=255, blank=True)
    address_number = models.CharField(_("Number"), max_length=20, blank=True)
    address_zip = models.CharField(_("Zip Code"), max_length=20, blank=True)
    address_city = models.CharField(_("City"), max_length=255, blank=True)
    address_country = CountryField(_("Country"), default='BE', max_length=255, blank=True)
    accountant = models.ForeignKey('accountant.Accountant', blank=True, null=True, on_delete=models.CASCADE)
    objects = CustomUserManager()
    simulation = models.ForeignKey(Simulation, blank=True, null=True, on_delete='cascade')
    valid = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_empty_fields(self):
        empty_fields = []
        if not (self.address_street and self.address_zip and self.address_city):
            empty_fields.append(_('your address'))
        if not self.telephone:
            empty_fields.append(_('your phonenumber'))
        if not self.id_card:
            empty_fields.append(_('a copy of your ID card'))
        if empty_fields :
            return empty_fields
        else:
            return None

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        self.valid = not self.get_empty_fields()
        for c in self.companies.all():
            c.valid_user = not self.get_empty_fields()
            c.save()
        super(CustomUser, self).save(*args, **kwargs)


    def send_adjusted_proposition(self, user):
        print("J'envoi le mail de confirmation")

        subject = _('[mylieutenantguillaume] Proposal')
        msg_html = render_to_string('acc_confirm_proposal.html', {
            'user': user,
            'domain': 'www.mylieutenantguillaume.com',  # current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        msg_txt = render_to_string('acc_confirm_proposal.txt', {
            'user': user,
            'domain': 'www.mylieutenantguillaume.com',  # current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to = self.email
        reply_to = "info@lieutenantguillaume.com"
        print(msg_txt)
        send_mail_smtp(str(subject), to, reply_to, msg_txt, msg_html)
