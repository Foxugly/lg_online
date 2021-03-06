# Generated by Django 2.2.13 on 2020-10-29 14:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accountant', '0002_accountant_slots'),
        ('agenda', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='back_customuser', to=settings.AUTH_USER_MODEL,
                                    verbose_name='Customer'),
        ),
        migrations.AddField(
            model_name='slot',
            name='refer_accountant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='back_accountant', to='accountant.Accountant',
                                    verbose_name='refer_accountant'),
        ),
        migrations.AddField(
            model_name='slot',
            name='st',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='agenda.SlotTemplate', verbose_name='Slot template'),
        ),
        migrations.AddField(
            model_name='daytemplate',
            name='slots',
            field=models.ManyToManyField(blank=True, to='agenda.SlotTemplate', verbose_name='Slots'),
        ),
    ]
