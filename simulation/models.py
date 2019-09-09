from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext as _


class Simulation(GenericClass):
    nb_invoice = models.IntegerField(_("Nombre annuel de de factures"))


    def __str__(self):
        return '%s' % (self.id)

    class Meta:
        verbose_name = _('Simulation')
