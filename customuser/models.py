from django.db import models
from tools.generic_class import GenericClass
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings


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
    enterprise_number = models.CharField(_("Enterprise Number"), max_length=12, null=True)
    enterprise_status = models.CharField(_("Enterprise Status"), max_length=12, blank=True)
    legal_situation = models.CharField(_("Legal Situation"), max_length=50, blank=True)
    start_date = models.DateField(_("Start date"), blank=True, null=True)
    enterprise_name = models.CharField(_("Enterprise Status"), max_length=255, blank=True)
    social_address_street = models.CharField(_("Street"), max_length=255, blank=True)
    social_address_number = models.CharField(_("Number"), max_length=20, blank=True)
    social_address_zip = models.CharField(_("Zip Code"), max_length=20, blank=True)
    social_address_city = models.CharField(_("City"), max_length=255, blank=True)
    social_address_country = models.CharField(_("Country"), max_length=255, blank=True)
    legal_form = models.CharField(_("Legal form"), max_length=255, blank=True)
    end_fiscal_date = models.CharField(_("End fiscal date"), max_length=50, blank=True)
    language = models.CharField(_("language"), max_length=8, choices=settings.LANGUAGES, default=1)
    is_foo_admin = models.BooleanField(_("Foo admin"), default=False, help_text=_('Designates users that are foo Admin.'),)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
