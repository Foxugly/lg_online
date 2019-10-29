from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext as _
from vies.validators import VATINValidator


class Company(GenericClass):
    enterprise_name = models.CharField(_("Enterprise Name"), max_length=255, blank=True)
    enterprise_number = models.CharField(_("Enterprise Number"), max_length=30, null=True, validators=[VATINValidator(verify=True, validate=True)])
    enterprise_status = models.CharField(_("Enterprise Status"), max_length=12, blank=True)
    legal_situation = models.CharField(_("Legal Situation"), max_length=50, blank=True)
    start_date = models.DateField(_("Start date"), blank=True, null=True)
    legal_form = models.CharField(_("Legal form"), max_length=255, blank=True)
    end_fiscal_date = models.CharField(_("End fiscal date"), max_length=50, blank=True)
    social_address_street = models.CharField(_("Street"), max_length=255, blank=True)
    social_address_number = models.CharField(_("Number"), max_length=20, blank=True)
    social_address_zip = models.CharField(_("Zip Code"), max_length=20, blank=True)
    social_address_city = models.CharField(_("City"), max_length=255, blank=True)
    social_address_country = models.CharField(_("Country"), max_length=255, blank=True)

    def __str__(self):
        return '[%s] %s' % (self.enterprise_number, self.enterprise_name if self.enterprise_name else None)

    class Meta:
        verbose_name = _('Company')


class Iban(GenericClass):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    iban = models.CharField(_("IBAN"), max_length=20, blank=True, null=True, )
    default = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.iban)

    class Meta:
        verbose_name = _('Iban')
