from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext as _
import math


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

coef_sector = {'horeca':0.95, 'management':1.15, 'liberal':1.2, 'construction':1.05, 'immo':1.15, 'assurances': 1.25, 'informatique': 1.3, 
        'retails': 0.95, 'avocat': 1.2, 'design': 1.3, 'architecte': 1.15, 'marketing' : 1.1}

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
    turnover = models.PositiveIntegerField(_("Chiffre d'affaires"))
    transmission = models.CharField(_("Mode de transmission des documents"), max_length=20, choices=TRANSMISSION_CHOICES)
    nb_invoices_sale = models.PositiveIntegerField(_("Nombre de factures de vente annuels"))
    nb_invoices_purchase = models.PositiveIntegerField(_("Nombre de factures d'achat et tickets annuels"))
    nb_managers = models.PositiveIntegerField(_("Nombre de dirigeants"))
    nb_employees = models.PositiveIntegerField(_("Nombre d'employers"))
    nb_creditcard = models.PositiveIntegerField(_("Nombre de carte de credits"))
    alternatif_payments = models.BooleanField(_("Système de paiements alternatifs (Paypal, Sumup, Stripe, ...)"))
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    tax_liability = models.CharField(max_length=20, choices=TAX_LIABILITY_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    
    def compute(self):
        V_CA = 0
        if self.turnover >= 1000000:
            V_CA = 1.5
        elif self.turnover >= 750000:
            V_CA = 1.4
        elif self.turnover >= 500000:
            V_CA = 1.3
        elif self.turnover >= 250000:
            V_CA = 1.2
        else:
            V_CA = 1
        V_nb_invoices_sale = 0.7 * self.nb_invoices_sale
        V_nb_invoices_purchase = 2.5 * self.nb_invoices_purchase
        V_nb_managers = 1500
        V_nb_employees = 100 * self.nb_employees
        V_nb_creditcard = 360 * self.nb_creditcard
        V_transmission = 480 if self.transmission == "paper" else 0
        V_alternatif_payments = 0 if not self.alternatif_payments else 300
        s = V_nb_invoices_sale + V_nb_invoices_purchase + V_transmission + V_nb_managers + V_nb_employees + \
            V_nb_creditcard + V_alternatif_payments
        max_calulated = (s * V_CA * coef_sector[self.sector] * coef_tax_liability[self.tax_liability])/12
        return max(200, math.ceil(max_calulated)), max_calulated

    def __str__(self):
        return '%s' % (self.id)

    class Meta:
        verbose_name = _('Simulation')
