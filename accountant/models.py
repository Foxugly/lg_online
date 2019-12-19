from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from timezone_field import TimeZoneField
from address.models import Address
from agenda.models import WeekTemplate, Slot


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
    telephone = PhoneNumberField(_("Phone number"), blank=True, null=True, help_text='format : +3221234567')
    default = models.BooleanField()
    view_busy_slot = models.BooleanField(default="False")
    colorslots = models.ManyToManyField(ColorSlot, verbose_name=_(u'ColorSlot'), blank=True)
    timezone = TimeZoneField(default=settings.TIME_ZONE)
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.CASCADE)
    weektemplate = models.ForeignKey(WeekTemplate, verbose_name=_(u'Week template'), blank=True, null=True, on_delete=models.CASCADE)
    slots = models.ManyToManyField(Slot, verbose_name=_(u'slots'), blank=True)

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

    def get_all_slottemplates(self):
        out = []
        if len(self.get_weektemplate().days.all()) > 0:
            for dt in self.get_weektemplate().days.all():
                for s in dt.slots.all():
                    out.append(s.as_json(dt.day, self))
        return out

    def remove_all_slottemplates(self):
        self.get_weektemplate().remove_all_slottemplates()

    def get_weektemplate(self):
        if not self.weektemplate:
            wt = WeekTemplate()
            wt.save()
            self.weektemplate = wt
            self.save()
        return self.weektemplate

    def get_daytemplate(self, i):
        return self.get_weektemplate().get_daytemplate(i)