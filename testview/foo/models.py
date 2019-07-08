from django.db import models
from django.urls import reverse


# Create your models here.
class Foo(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")

    def get_absolute_url(self):
        return reverse('foo:foo_change', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse('foo:foo_detail', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('foo:foo_delete', kwargs={'pk': self.pk})

    def add_url(self):
        return reverse('foo:foo_add')

    def list_url(self):
        return reverse('foo:foo_list')

    def __str__(self):
        return self.name
