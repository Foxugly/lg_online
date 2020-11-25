from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField

from company.models import Company
from tools.generic_class import GenericClass


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
    simulation = models.ForeignKey('simulation.Simulation', blank=True, null=True, on_delete=models.CASCADE)
    valid = models.BooleanField(default=False)
    schedule_meeting = models.BooleanField(default=True)
    timezone = TimeZoneField(default=settings.TIME_ZONE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_company_name(self):
        return self.companies.all()[0].enterprise_name

    def get_company_number(self):
        return self.companies.all()[0].enterprise_number

    def get_company_url(self):
        return self.companies.all()[0].get_absolute_url()

    def get_simulation_url(self):
        return self.simulation.get_absolute_url()

    def get_empty_fields(self):
        empty_fields = []
        if not (self.address_street and self.address_zip and self.address_city):
            empty_fields.append(_('votre adresse'))
        if not self.telephone:
            empty_fields.append(_('votre numéro de téléphone'))
        if not self.id_card:
            empty_fields.append(_("une copie de votre carte d'identité"))
        if empty_fields:
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
