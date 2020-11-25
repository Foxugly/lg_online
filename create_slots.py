from datetime import date, timedelta

from accountant.models import Accountant
from agenda.models import SlotTemplate, DayTemplate, WeekTemplate, Slot

wt = WeekTemplate()
wt.save()
for i in range(1, 6):
    dt = DayTemplate(day=i)
    dt.save()
    st1 = SlotTemplate(start="8:00:00", end="8:30:00", slot_type=1)
    st1.save()
    dt.slots.add(st1)
    st2 = SlotTemplate(start="8:30:00", end="9:00:00", slot_type=1)
    st2.save()
    dt.slots.add(st2)
    st3 = SlotTemplate(start="9:00:00", end="9:30:00", slot_type=1)
    st3.save()
    dt.slots.add(st3)
    st4 = SlotTemplate(start="9:30:00", end="10:00:00", slot_type=1)
    st4.save()
    dt.slots.add(st4)
    st5 = SlotTemplate(start="10:00:00", end="10:30:00", slot_type=1)
    st5.save()
    dt.slots.add(st5)
    st6 = SlotTemplate(start="10:30:00", end="11:00:00", slot_type=1)
    st6.save()
    dt.slots.add(st6)
    st7 = SlotTemplate(start="11:00:00", end="11:30:00", slot_type=1)
    st7.save()
    dt.slots.add(st7)
    st8 = SlotTemplate(start="11:30:00", end="12:00:00", slot_type=1)
    st8.save()
    dt.slots.add(st8)
    wt.days.add(dt)
    wt.save()

start_date = date(2019, 12, 16)
end_date = date(2019, 12, 27)
accountant = Accountant.objects.get(pk=1)
accountant.weektemplate = wt
accountant.save()
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

for i in range(0, 7):
    print("create slots for %s" % days[i])
    current_day = start_date + timedelta(days=i)
    while current_day <= end_date:
        sts = accountant.get_daytemplate(
            1 + (int(start_date.weekday()) + i) % 7).get_slottemplates()
        if sts:
            for st in sts:
                new_slot = Slot(date=current_day, st=st, refer_accountant=accountant, booked=st.booked)
                new_slot.save()
        current_day += timedelta(days=7)
