# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.urls import path
from agenda.views import st_add, st_remove, st_apply, st_clean, get_slot, book_slot, remove_slot, clean_slot, CalendarListView
from django.contrib.auth.decorators import login_required

app_name = 'agenda'
urlpatterns = (
	path('', CalendarListView.as_view(), name='slot_list'),
	#path('<int:accountant_id>/', calendar, name='calendar'),
    path('ajax/s/get/<int:slot_id>/', get_slot, name='get_slot'),
    path('ajax/st/add/', login_required(st_add), name='st_add'),
    path('ajax/st/clean/', login_required(st_clean), name='st_clean'),
    path('ajax/st/apply/', login_required(st_apply), name='st_apply'),
    path('ajax/st/remove/<int:st_id>/', login_required(st_remove), name='st_remove'),
    path('ajax/s/book/<int:slot_id>/', book_slot, name='book_slot'),
    path('ajax/s/remove/<int:slot_id>/', login_required(remove_slot), name='remove_slot'),
    path('ajax/s/clean/<int:slot_id>/', login_required(clean_slot), name='clean_slot'),
)
