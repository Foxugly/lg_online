# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.conf import settings
from agenda.models import SlotTemplate, Slot
from accountant.models import Accountant
import json
from tools.toolbox import string_random
from multiprocessing import Process
from threading import Thread
from django.db import connection
from django.template.loader import render_to_string
from django.shortcuts import render
from tools.generic_views import GenericListView
from django.urls import reverse_lazy
from tools.mail import send_mail_smtp
from django.utils.translation import gettext_lazy as _


class CalendarListView(GenericListView):
    model = Slot
    paginate_by = None
    template_name = 'calendar.html'
    crumbs = [('Agenda', reverse_lazy('agenda:slot_list'))]  # OR reverse_lazy

    def get_queryset(self):
        accountant = self.request.user.accountant
        today = datetime.now().date()
        l_slots = []
        if accountant.view_busy_slot :
            slots = slot.objects.filter(date__gte=today, refer_accountant=accountant)
        else:
            slots = Slot.objects.filter(date__gte=today, refer_accountant=accountant, customer__isnull=True)
        for s in slots:
            l_slots.append(s.as_json())
        return l_slots


@login_required
def st_add(request):
    if request.is_ajax():
        days = ['check_monday', 'check_tuesday', 'check_wednesday', 'check_thursday', 'check_friday', 'check_saturday',
                'check_sunday']
        results = {}
        for day in days:
            if day in request.POST:
                dt = request.user.get_daytemplate(days.index(day) + 1)
                current = datetime.strptime(settings.FULLCALENDAR_REF_DATE + ' ' + request.POST['start_time'],
                                            "%Y-%m-%d %H:%M")
                current += timedelta(days=days.index(day))
                end = datetime.strptime(settings.FULLCALENDAR_REF_DATE + ' ' + request.POST['end_time'],
                                        '%Y-%m-%d %H:%M')
                end += timedelta(days=days.index(day))
                while current < end:
                    current_end = current + timedelta(minutes=int(request.POST['duration']))
                    if dt.n_slottemplates() > 0:
                        for old_slot in dt.slots.filter(start__lte=current, end__gt=current):
                            dt.slots.remove(old_slot)
                        for old_slot in dt.slots.filter(start__lt=current_end, end__gte=current_end):
                            dt.slots.remove(old_slot)
                    booked = True if request.POST['booked'] == "1" else False
                    st = SlotTemplate(start=current, end=current_end, slot_type=request.POST['slot_type'],
                                      booked=booked)
                    st.save()
                    dt.add_slottemplate(st)
                    current = current_end + timedelta(minutes=int(request.POST['break_time']))
        results['return'] = True
        results['slottemplates'] = request.user.get_all_slottemplates()
        return HttpResponse(json.dumps(results))


@login_required
def st_clean(request):
    if request.is_ajax():
        request.user.remove_all_slottemplates()
        results = {'slottemplates': request.user.get_all_slottemplates(), 'return': True}
        return HttpResponse(json.dumps(results))


class ApplySlots(Thread):
    def __init__(self, start_date, end_date, accountant):
        Thread.__init__(self)
        self.start_date = start_date
        self.end_date = end_date
        self.accountant = accountant

    def run(self):
        #apply_slots(start_date, end_date, accountant):
        for i in range(0, 7):
            current_day = self.start_date + timedelta(days=i)
            while current_day <= self.end_date:
                sts = self.accountant.get_daytemplate(
                        1 + (int(self.start_date.weekday()) + i) % 7).get_slottemplates()
                if sts:
                    for st in sts:
                        current_day = current_day.replace(hour=st.start.hour, minute=st.start.minute)
                        for s in self.accountant.slots.filter(date=datetime.date(current_day), st__start__lte=current_day,
                                                  st__end__gt=current_day):
                            self.accountant.slots.remove(s)
                        current_day = current_day.replace(hour=st.end.hour, minute=st.end.minute)
                        for s in self.accountant.slots.filter(date=datetime.date(current_day), st__start__lt=current_day,
                                                  st__end__gte=current_day):
                            self.accountant.slots.remove(s)
                        new_slot = Slot(date=datetime.date(current_day), st=st, refer_accountant=self.accountant, booked=st.booked)
                        new_slot.save()
                        self.accountant.slots.add(new_slot)
                current_day += timedelta(days=7)


@login_required
def st_apply(request):
    results = {}
    if request.is_ajax():
        if 'start_date' in request.POST and 'end_date' in request.POST and request.POST['start_date'] and request.POST['end_date']:
            start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
            connection.close()
            # p = Process(target=apply_slots, args=(start_date, end_date, request.user))
            # apply_slots(start_date, end_date, request.user)
            ap = ApplySlots(start_date, end_date, request.user)
            ap.start()
            # p.start()
            results['return'] = True
        else:
            results['return'] = False
        return HttpResponse(json.dumps(results))


@login_required
def st_remove(request, st_id):
    results = {}
    if request.is_ajax():
        st = SlotTemplate.objects.get(id=int(st_id))
        for dt in request.user.weektemplate.days.all():
            dt.remove_slottemplate(st)
        results['return'] = True
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))


def get_slot(request, slot_id):
    results = {}
    if request.is_ajax():
        s = Slot.objects.get(id=int(slot_id))
        if request.user.is_authenticated:
            results['slot'] = s.detail()
            results['return'] = True
        else:
            if not s.booked:
                results['return'] = True
                results['slot'] = s.detail()
            else:
                results['return'] = False
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))


def book_slot(request, slot_id):
    if request.is_ajax():
        s = Slot.objects.get(id=slot_id)
        s.customer = request.user
        s.booked = True
        s.save()
        s.icalendar()
        msg_txt = render_to_string('mail/mail_meeting.txt', {'user': s.customer})
        send_mail_smtp("[LG&Associates] icalendar of meeting", [s.customer.email, s.refer_accountant.email], None, msg_txt, None, [s.path])
        # send_mail_smtp(_("[LG&Associates] icalendar of meeting"), [s.customer.email, s.refer_accountant.email], None, msg_txt, None, [s.path])
        request.user.schedule_meeting = False
        request.user.save()
        d = {'return': True, 'slot': s.as_json()}
        return HttpResponse(json.dumps(d))


@login_required
def remove_slot(request, slot_id):
    if request.is_ajax():
        slot = Slot.objects.get(id=slot_id)
        # if slot.customer:
        #    mail_customer_cancel_appointment_from_accountanttor(request, slot)
        #    TODO
        slot.delete()
        return HttpResponse(json.dumps({'return': True}))


@login_required
def clean_slot(request, slot_id):
    if request.is_ajax():
        slot = Slot.objects.get(id=slot_id)
        #if slot.customer:
        #   mail_customer_cancel_appointment_from_accountanttor(request, slot)
        #   TODO
        slot.clean_slot()
        d = {'return': True, 'slot': slot.as_json()}
        return HttpResponse(json.dumps(d))
