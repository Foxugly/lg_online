# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.urls import path

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import CustomUserCreateView, CustomUserUpdataDataView, activate

app_name = 'customuser'

urlpatterns = [
    path('add/', CustomUserCreateView.as_view(), name='customuser_add'),
    path('update/', CustomUserUpdataDataView.as_view(), name='update_data'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
]
