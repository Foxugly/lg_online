# Generated by Django 2.2.13 on 2020-10-29 14:25

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accountant', '0001_initial'),
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountant',
            name='slots',
            field=models.ManyToManyField(blank=True, to='agenda.Slot', verbose_name='slots'),
        ),
    ]
