from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Contact(GenericClass):
    name = models.CharField(_("name"), max_length=50, blank=True)
    email = models.CharField(_("email"), max_length=50, blank=True, null=True,)
    telephone = PhoneNumberField(_("Phone number"), blank=True, null=True,)
    default = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Contact')