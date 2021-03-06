# Generated by Django 2.2.13 on 2020-10-30 08:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('simulation', '0001_initial'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='calculated_amount',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Mensualité calculée'),
        ),
        migrations.AddField(
            model_name='company',
            name='date_calculated_amount',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='simulation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='simulation.Simulation'),
        ),
    ]
