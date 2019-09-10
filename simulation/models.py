from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext as _

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

coef_sector = {'horeca':0.8, 'management':1, 'liberal':1.1, 'construction':0.9, 'immo':1.2, 'assurances': 1.1, 'informatique': 1.2, 
        'retails': 0.7, 'avocat': 1.4, 'design': 1.1, 'architecte': 1, 'marketing' : 1.1}

TAX_LIABILITY_CHOICES = (
    ('monthly': _("mensuellement")),
    ('quarterly' : _("trimestriellement")),
    ('none', : _("Non déposant")),
)

coef_tax_liability = {'monthly': 1.3, 'quarterly':1, 'none': 0.8}


class Simulation(GenericClass):
    nb_documents = models.IntegerField(_("Nombre de documents annuels (factures de vente, factures d'achat et tickets)"))
    nb_managers =  = models.IntegerField(_("Nombre de dirigeants"))
    nb_employees = models.IntegerField(_("Nombre d'employers"))
    nb_creditcard = models.IntegerField(_("Nombre de carte de credits"))
    alternatif_payments = models.BooleanField(_("Système de paiements alternatifs (Paypal, Sumup, Stripe, ...)"))
    sector = models.models.CharField(max_length=20, choices=SECTOR_CHOICES)
    tax_liability = models.models.CharField(max_length=20, choices=TAX_LIABILITY_CHOICES)
    
    def compute(self):
        V_nb_docs = 1,7 * self.nb_documents
        V_nb_managers = 360 * self.nb_managers
        V_nb_employees = 0 if self.nb_employees == 0 else (100 * self.nb_employees) + 100
        V_nb_creditcard = 160 * self.nb_creditcard
        V_alternatif_payments = 0 if not self.alternatif_payments else 600
        s = V_nb_docs + V_nb_managers + V_nb_employees + V_nb_creditcard + V_alternatif_payment
        total = max(200, (s * coef_sector[self.sector] * coef_tax_liability[self.tax_liability])/12)
        return total      

    def __str__(self):
        return '%s' % (self.id)

    class Meta:
        verbose_name = _('Simulation')
