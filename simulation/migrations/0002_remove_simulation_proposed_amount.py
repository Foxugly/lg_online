# Generated by Django 2.2.13 on 2020-10-30 09:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('simulation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulation',
            name='proposed_amount',
        ),
    ]
