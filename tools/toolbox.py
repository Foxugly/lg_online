# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

# import os
import random
import string
# import tempfile


# from django.conf import settings


def string_random(size):
    s = string.ascii_letters + string.digits
    return ''.join(random.sample(s, size))


def mail():
    return None


def convert_date(s):
    out = s
    out = out.replace('yyyy', '%Y')
    out = out.replace('yy', '%y')
    out = out.replace('mm', '%m')
    out = out.replace('dd', '%d')
    return out
