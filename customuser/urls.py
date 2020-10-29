# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.urls import path
from customuser.views import activate, confirm_proposal
from tools.generic_urls import add_url_from_generic_views
from customuser.views import ProfileUpdateView

app_name = 'customuser'

urlpatterns = [
    path('profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('confirm/<str:uidb64>/<str:token>/', confirm_proposal, name='confirm_proposal'),
] + add_url_from_generic_views('customuser.views')
