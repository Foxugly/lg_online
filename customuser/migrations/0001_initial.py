# Generated by Django 2.2.13 on 2020-10-29 14:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('simulation', '0001_initial'),
        ('accountant', '0002_accountant_slots'),
        ('company', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Français'), ('nl', 'Nederlands')], default=1, max_length=8, verbose_name='language')),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=20, region=None, verbose_name='Phone number')),
                ('id_card', models.FileField(blank=True, upload_to='idcard/')),
                ('address_street', models.CharField(blank=True, max_length=255, verbose_name='Street')),
                ('address_number', models.CharField(blank=True, max_length=20, verbose_name='Number')),
                ('address_zip', models.CharField(blank=True, max_length=20, verbose_name='Zip Code')),
                ('address_city', models.CharField(blank=True, max_length=255, verbose_name='City')),
                ('address_country', django_countries.fields.CountryField(blank=True, default='BE', max_length=255, verbose_name='Country')),
                ('valid', models.BooleanField(default=False)),
                ('schedule_meeting', models.BooleanField(default=True)),
                ('timezone', timezone_field.fields.TimeZoneField(default='Europe/Brussels')),
                ('accountant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accountant.Accountant')),
                ('companies', models.ManyToManyField(blank=True, to='company.Company', verbose_name='companies')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('simulation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='simulation.Simulation')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
