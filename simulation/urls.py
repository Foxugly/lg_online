# -*- coding: utf-8 -*-
#
# Copyright 2019, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.urls import path

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import SimulationCreateView, SimulationUpdateView, send_simulation_by_mail


app_name = 'simulation'

urlpatterns = [
    path('', SimulationCreateView.as_view(), name='simulation_add'),
    path('<int:pk>/', SimulationUpdateView.as_view(), name='simulation_change'),
    path('ajax/send_mail/', send_simulation_by_mail, name='send_simulation_by_mail'),
    
]