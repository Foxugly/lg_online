# Generated by Django 2.2.13 on 2020-10-29 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(1, 'Lundi'), (2, 'Mardi'), (3, 'Mercredi'), (4, 'Jeudi'), (5, 'Vendredi'), (6, 'Samedi'), (7, 'Dimanche')], verbose_name='Day')),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('informations', models.TextField(blank=True, null=True, verbose_name='Usefull informations')),
                ('booked', models.BooleanField(default=False, verbose_name='Booked')),
                ('random', models.CharField(blank=True, max_length=16, null=True, verbose_name='random character')),
                ('path', models.CharField(blank=True, max_length=255, null=True, verbose_name='path_ics')),
            ],
        ),
        migrations.CreateModel(
            name='SlotTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField(verbose_name='Start')),
                ('end', models.TimeField(verbose_name='End')),
                ('slot_type', models.IntegerField(choices=[(1, 'Premier RDV')], verbose_name='Slot type')),
                ('booked', models.BooleanField(default=False, verbose_name='Booked')),
            ],
        ),
        migrations.CreateModel(
            name='WeekTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.ManyToManyField(blank=True, to='agenda.DayTemplate', verbose_name='Days')),
            ],
        ),
    ]
