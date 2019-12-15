from django.contrib import admin
from accountant.models import Accountant, ColorSlot


class AccountantAdmin(admin.ModelAdmin):
    pass



class ColorSlotAdmin(admin.ModelAdmin):
    pass

admin.site.register(Accountant, AccountantAdmin)
admin.site.register(ColorSlot, ColorSlotAdmin)