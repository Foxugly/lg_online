from django import template


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

#@register.filter(name='verbose_name')
#def verbose_name(obj):
#    return obj.verbose_name


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
    return date.strftime(formats.get_format('DATE_INPUT_FORMATS')[0])


@register.filter()
def filename(path):
    return os.path.basename(path.name)


@register.filter()
def cast(s):
    return s.replace(' ', '+')


@register.filter()
def after_today(date):
    return date > datetime.today()


@register.filter()
def file_exists(path):
    if path:
        return os.path.exists(path)
    else:
        return False