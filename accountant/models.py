from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class ColorSlot(models.Model):
    SLOT_TYPE = settings.SLOT_TYPE
    slot = models.IntegerField(verbose_name=_(u'Type of slot'), choices=SLOT_TYPE)
    free_slot_color = models.CharField(verbose_name=_(u'Free pricing free slot color'), default='#73B5EB', max_length=8)
    booked_slot_color = models.CharField(verbose_name=_(u'Booked slot color'), default='#F64636', max_length=8)

    def __str__(self):
        return ' %d - %d' % (self.id, self.slot)


class Accountant(GenericClass):
    name = models.CharField(_("name"), max_length=50, blank=True)
    email = models.CharField(_("email"), max_length=50, blank=True, null=True,)
    telephone = PhoneNumberField(_("Phone number"), blank=True, null=True,)
    default = models.BooleanField()
    view_busy_slot = models.BooleanField(default="False")
    colorslots = models.ManyToManyField(ColorSlot, verbose_name=_(u'ColorSlot'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Comptable')


    def get_colorslot(self, i):
        ret = None
        if self.get_n_colorslots() > 0:
            for cs in self.colorslots.all():
                if cs.slot == i:
                    ret = cs
        if ret is None:
            ret = ColorSlot(slot=i, free_slot_color=settings.SLOT_COLOR[i - 1])
            ret.save()
            self.colorslots.add(ret)
            self.save()
        return ret

    def get_n_colorslots(self):
        return len(self.colorslots.all())
        
    def get_color(self, i, booked):
        slot = self.get_colorslot(i)
        return str(slot.booked_slot_color) if booked else str(slot.free_slot_color)