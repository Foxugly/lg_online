from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext as _
import math
from django.utils import timezone


SECTOR_CHOICES = (
    ('horeca', _("Horeca")),
    ('management', _("Société de management")),
    ('liberal', _("Profession libérale")),
    ('construction', _("Construction")),
    ('immo', _("Immobilière / Patrimoniale")),
    ('assurances', _("Assurances")),
    ('informatique', _("Informatique")),
    ('retails', _("Retails")),
    ('avocat', _("Avocat")),
    ('design', _("Design")),
    ('architecte', _("Architecte")),
    ('marketing', _("Marketing")),
)

coef_sector = {'horeca': 0.95, 'management': 1.15, 'liberal': 1.2, 'construction': 1.05, 'immo': 1.15,
               'assurances': 1.25, 'informatique': 1.3, 'retails': 0.95, 'avocat': 1.2, 'design': 1.3,
               'architecte': 1.15, 'marketing': 1.1}

TAX_LIABILITY_CHOICES = (
    ('monthly', _("mensuellement")),
    ('quarterly', _("trimestriellement")),
    ('none', _("Non déposant")),
)

TRANSMISSION_CHOICES = (
    ('online', _("En ligne")),
    ('paper', _("Papier")),
)

coef_tax_liability = {'monthly': 1.5, 'quarterly': 1.3, 'none': 1}


class Simulation(GenericClass):
    turnover = models.PositiveIntegerField(_("Chiffre d'affaires"), blank=False, default=50000)
    transmission = models.CharField(_("Mode de transmission des documents"), max_length=20,
                                    choices=TRANSMISSION_CHOICES, blank=False, default='online')
    nb_invoices_sale = models.PositiveIntegerField(_("Nombre de factures de vente annuels"), blank=False, default=200)
    nb_invoices_purchase = models.PositiveIntegerField(_("Nombre de factures d'achat et tickets annuels"),
                                                       blank=False, default=200)
    nb_managers = models.PositiveIntegerField(_("Nombre de dirigeants"), blank=False, default=1)
    nb_employees = models.PositiveIntegerField(_("Nombre d'employers"), blank=False, default=0)
    nb_creditcard = models.PositiveIntegerField(_("Nombre de carte de credits"), blank=False, default=1)
    alternatif_payments = models.BooleanField(_("Système de paiements alternatifs (Paypal, Sumup, Stripe, ...)"),
                                              blank=False)
    sector = models.CharField(_("Secteur d'activité"), max_length=20, choices=SECTOR_CHOICES, default="horeca")
    tax_liability = models.CharField(_("Fréquence de déclaration TVA"), max_length=20, choices=TAX_LIABILITY_CHOICES,
                                     default='quarterly')
    calculated_amount = models.PositiveIntegerField(_("Mensualité calculée"), blank=True, default=0)
    date_calculated_amount = models.DateTimeField(blank=True, null=True)
    #proposed_amount = models.PositiveIntegerField(_("Mensualité proposée"), blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def compute(self):
        v_ca = 1
        if self.turnover >= 1000000:
            v_ca = 1.5
        elif self.turnover >= 750000:
            v_ca = 1.4
        elif self.turnover >= 500000:
            v_ca = 1.3
        elif self.turnover >= 250000:
            v_ca = 1.2
        v_nb_invoices_sale = 0.7 * self.nb_invoices_sale
        v_nb_invoices_purchase = 2.5 * self.nb_invoices_purchase
        v_nb_managers = 1500
        v_nb_employees = 100 * self.nb_employees
        v_nb_creditcard = 360 * self.nb_creditcard
        v_transmission = 480 if self.transmission == "paper" else 0
        v_alternatif_payments = 0 if not self.alternatif_payments else 300
        s = v_nb_invoices_sale + v_nb_invoices_purchase + v_transmission + v_nb_managers + v_nb_employees + \
            v_nb_creditcard + v_alternatif_payments
        max_calulated = (s * v_ca * coef_sector[self.sector] * coef_tax_liability[self.tax_liability])/12
        return max_calulated

    def compute_with_max(self):
        return max(200, math.ceil(self.compute()))

    def update(self):
        self.proposed_amount = self.compute_with_max()
        self.save()

    def save(self, *args, **kwargs):
        if self.calculated_amount == 0:
            self.calculated_amount = max(200, self.compute_with_max())
            self.date_calculated_amount = timezone.now()
            self.proposed_amount = self.calculated_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.pk

    class Meta:
        verbose_name = _('Ma simulation personnalisée')
        # detail_name = _('Essayez de renseigner chaque indicateur avec des chiffres au plus près de votre activité pour avoir une estimation la plus fidèle possible.')
