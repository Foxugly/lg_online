from django.db import models
from django.utils.translation import gettext as _
from django_countries.fields import CountryField


class Address(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False)
    street = models.CharField(_("Street"), max_length=255, blank=True)
    number = models.CharField(_("Number"), max_length=20, blank=True)
    zipcode = models.CharField(_("Zip Code"), max_length=20, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    country = CountryField(_("Country"), default='BE', max_length=255, blank=True)

    def __str__(self):
        return self.name

    def formatted(self):
        return "%s %s, %s %s, %s" % (self.street, self.number, self.zipcode, self.city, self.country)
