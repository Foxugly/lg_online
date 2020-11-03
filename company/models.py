from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext as _
from vies.validators import VATINValidator
from django_countries.fields import CountryField
from localflavor.generic.models import IBANField


class Company(GenericClass):
    END_FISCAL_DATE_CHOICES = [
        ("1", _('31 mars')),
        ("2", _('30 juin')),
        ("3", _('30 septembre')),
        ("4", _('31 décembre')),
        ("0", _('autre')),
    ]

    enterprise_name = models.CharField(_("Enterprise Name"), max_length=255, blank=True)
    enterprise_number = models.CharField(_("Enterprise Number"), max_length=30, null=True,
                                         validators=[VATINValidator(verify=True)])
    enterprise_status = models.CharField(_("Enterprise Status"), max_length=12, blank=True)
    legal_situation = models.CharField(_("Legal Situation"), max_length=50, blank=True)
    start_date = models.DateField(_("Start date"), blank=True, null=True)
    legal_form = models.CharField(_("Legal form"), max_length=255, blank=True)
    end_fiscal_date = models.CharField(_("End fiscal date"), max_length=50, choices=END_FISCAL_DATE_CHOICES,
                                       default=4, )
    social_address_street = models.CharField(_("Street"), max_length=255, blank=True)
    social_address_number = models.CharField(_("Number"), max_length=20, blank=True)
    social_address_zip = models.CharField(_("Zip Code"), max_length=20, blank=True)
    social_address_city = models.CharField(_("City"), max_length=255, blank=True)
    social_address_country = CountryField(_("Country"), default='BE', max_length=255, blank=True)
    accountant = models.ForeignKey('accountant.Accountant', blank=True, null=True, on_delete=models.CASCADE)
    valid = models.BooleanField(default=False)
    valid_user = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    calculated_amount = models.PositiveIntegerField(_("Mensualité calculée"), blank=True, default=0)
    date_calculated_amount = models.DateTimeField(blank=True, null=True)
    proposed_amount = models.PositiveIntegerField(_("Mensualité proposée"), blank=True, default=0)
    simulation = models.ForeignKey('simulation.Simulation', blank=True, null=True, on_delete=models.CASCADE)
    accountant = models.ForeignKey('accountant.Accountant', blank=True, null=True, on_delete=models.CASCADE)

    def get_simulation_price(self):
        return self.proposed_amount

    def get_empty_fields(self):
        empty_fields = []
        if not (
                self.social_address_street and self.social_address_zip and self.social_address_city and self.social_address_country):
            empty_fields.append(_('your address'))
        ibans = Iban.objects.filter(company=self)
        if not ibans:
            empty_fields.append(_('an iban account'))
        if empty_fields:
            if len(empty_fields) == 1:
                out = str(empty_fields[0])
            else:
                out = ", ".join(str(v) for v in empty_fields[:-1]) + " %s %s" % (_('and'), str(empty_fields[-1]))
            return out
        else:
            return None

    def save(self, *args, **kwargs):
        self.valid = not self.get_empty_fields()
        if self.valid and self.valid_user and not self.sent:
            self.sent = True
            print("GO TO FID YUKI CODABOX")
            # TODO FID YUKI CODABOX
            # TODO envoyé à contact : tu as un nouveau client
        super(Company, self).save(*args, **kwargs)

    def fill_data(self, data):
        if len(data):
            for key, value in data.items():
                if key == 'statut':
                    self.enterprise_status = value
                elif key == 'situation_juridique':
                    self.legal_situation = value
                elif key == 'date_debut':
                    self.start_date = value
                elif key == 'denomination':
                    self.enterprise_name = value
                elif key == 'adresse':
                    self.social_address_street = value
                elif key == 'adresse_num':
                    self.social_address_number = value
                elif key == 'adresse_cp':
                    self.social_address_zip = value
                elif key == 'adresse_ville':
                    self.social_address_city = value
                elif key == 'forme_legale':
                    self.legal_form = value
                elif key == 'date_fin_annee_comptable':
                    self.end_fiscal_date = value

    def __str__(self):
        return '[%s] %s' % (self.enterprise_number, self.enterprise_name if self.enterprise_name else None)

    class Meta:
        verbose_name = _('Mon entreprise')
        verbose_name_plural = _('Mes entreprises')


class Iban(GenericClass):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    iban = IBANField(_("Iban"), max_length=20, blank=True, null=True, )
    default = models.BooleanField(_("par défaut"), default=False)

    def __str__(self):
        return '%s' % self.iban

    class Meta:
        verbose_name = _('Iban')
