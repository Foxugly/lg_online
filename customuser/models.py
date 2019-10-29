from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from company.models import Company
from phonenumber_field.modelfields import PhoneNumberField
from contact.models import Contact
from simulation.models import Simulation


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


class CustomUser(AbstractUser):
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
    address_country = models.CharField(_("Country"), max_length=255, blank=True)
    contact = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.CASCADE)
    objects = CustomUserManager()
    simulation = models.ForeignKey(Simulation, blank=True, null=True, on_delete='cascade')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
