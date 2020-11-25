from django import template
from django.utils.translation import gettext as _

from simulation.models import translate_fields

register = template.Library()


# @register.filter(name='hash')
# def hash(h, key):
#    return h[key]


# @register.filter(name='dict')
# def dict(h):
#    return None

@register.filter(name='verbose_name')
def get_verbose_name(object):
    return object._meta.verbose_name


@register.filter(name='clean')
def clean(obj):
    out = None
    if type(obj) == bool:
        if obj == True:
            out = _("Oui")
        elif obj == False:
            out = _("Non")
    elif obj in translate_fields:
        out = translate_fields[obj]
    else:
        out = obj
    return out


@register.filter(name='app_name')
def app_name(obj):
    return obj.app_label


@register.filter()
def index(d, value):
    return dict(d)[value]


@register.filter()
def time_format(time):
    return u"%02d:%02d" % (time.hour, time.minute)


@register.filter()
def date_format(date):
    return date.strftime("%d/%m/%Y")
