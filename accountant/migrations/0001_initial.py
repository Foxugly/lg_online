# Generated by Django 2.2.13 on 2020-10-26 11:29

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.IntegerField(choices=[(1, 'Premier RDV')], verbose_name='Type of slot')),
                ('free_slot_color', models.CharField(default='#73B5EB', max_length=8, verbose_name='Free pricing free slot color')),
                ('booked_slot_color', models.CharField(default='#F64636', max_length=8, verbose_name='Booked slot color')),
            ],
        ),
        migrations.CreateModel(
            name='Accountant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='name')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='email')),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='format : +3221234567', max_length=128, null=True, region=None, verbose_name='Phone number')),
                ('default', models.BooleanField()),
                ('view_busy_slot', models.BooleanField(default='False')),
                ('timezone', timezone_field.fields.TimeZoneField(default='Europe/Brussels')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.Address')),
                ('colorslots', models.ManyToManyField(blank=True, to='accountant.ColorSlot', verbose_name='ColorSlot')),
            ],
            options={
                'verbose_name': 'Comptable',
            },
        ),
    ]
