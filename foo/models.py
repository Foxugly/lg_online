from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class Bar(GenericClass):
    name = models.CharField(max_length=100, verbose_name=_("name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Bar')


class Multibar(GenericClass):
    name = models.CharField(max_length=100, verbose_name=_("name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Multibar')


class Foo(GenericClass):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE, verbose_name=_("bar"))
    multibars = models.ManyToManyField(Multibar, blank=True, verbose_name=_("multibars"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Foo')
