# Generated by Django 2.2.13 on 2020-10-26 11:33

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import localflavor.generic.models
import vies.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accountant', '0002_accountant_slots'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enterprise_name', models.CharField(blank=True, max_length=255, verbose_name='Enterprise Name')),
                ('enterprise_number', models.CharField(max_length=30, null=True, validators=[vies.validators.VATINValidator(verify=True)], verbose_name='Enterprise Number')),
                ('enterprise_status', models.CharField(blank=True, max_length=12, verbose_name='Enterprise Status')),
                ('legal_situation', models.CharField(blank=True, max_length=50, verbose_name='Legal Situation')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start date')),
                ('legal_form', models.CharField(blank=True, max_length=255, verbose_name='Legal form')),
                ('end_fiscal_date', models.CharField(choices=[('1', '31 mars'), ('2', '30 juin'), ('3', '30 septembre'), ('4', '31 décembre'), ('0', 'autre')], default=4, max_length=50, verbose_name='End fiscal date')),
                ('social_address_street', models.CharField(blank=True, max_length=255, verbose_name='Street')),
                ('social_address_number', models.CharField(blank=True, max_length=20, verbose_name='Number')),
                ('social_address_zip', models.CharField(blank=True, max_length=20, verbose_name='Zip Code')),
                ('social_address_city', models.CharField(blank=True, max_length=255, verbose_name='City')),
                ('social_address_country', django_countries.fields.CountryField(blank=True, default='BE', max_length=255, verbose_name='Country')),
                ('valid', models.BooleanField(default=False)),
                ('valid_user', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
                ('accountant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accountant.Accountant')),
            ],
            options={
                'verbose_name': 'Mon entreprise',
                'verbose_name_plural': 'Mes entreprises',
            },
        ),
        migrations.CreateModel(
            name='Iban',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iban', localflavor.generic.models.IBANField(blank=True, include_countries=None, max_length=20, null=True, use_nordea_extensions=False, verbose_name='Iban')),
                ('default', models.BooleanField(default=False, verbose_name='par défaut')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company')),
            ],
            options={
                'verbose_name': 'Iban',
            },
        ),
    ]
