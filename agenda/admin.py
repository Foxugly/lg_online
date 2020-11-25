# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.contrib import admin

from agenda.models import Slot, DayTemplate, WeekTemplate, SlotTemplate


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    pass


@admin.register(DayTemplate)
class DayTemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('slots',)


@admin.register(WeekTemplate)
class WeekTemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('days',)


@admin.register(SlotTemplate)
class SlotTemplateAdmin(admin.ModelAdmin):
    pass
