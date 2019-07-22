from django.db import models
from tools.generic_class import GenericClass
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from company.models import Company
from phonenumber_field.modelfields import PhoneNumberField
from contact.models import Contact


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
    telephone = PhoneNumberField(_("Phone number"), blank=True)
    id_card = models.FileField(upload_to=settings.IDCARD_URL, blank=True)
    contact = models.ForeignKey(Contact, blank=True, null=True, on_delete='cascade')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
