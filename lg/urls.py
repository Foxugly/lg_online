"""boot4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib import admin
from django.urls import path, include, reverse
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import translation
from customuser.views import CustomUserUpdateView, CustomUserLoginView, MyPasswordResetView
from customuser.decorators import check_lang
from django.http import JsonResponse
from tools.mail import send_mail_smtp
from django.utils.translation import gettext_lazy as _


@check_lang
def home(request):
    #return calendar(request, request.user.accountant.pk)
    c = {}
    if request.user.is_authenticated:
        if request.user.is_active:
            if request.user.is_staff or request.user.is_superuser:
                return redirect('customuser:customuser_list')
            else:
                return redirect('company:company_list')
    else:
        return render(request, "index.html", c)


def comment_creation(request):
    c = {'title': _('Confirmation'), 'text': _('We just send you an email for validation.')}
    return render(request, "comment.html", c)


def set_language(request):
    if 'lang' in request.GET and 'next' in request.GET:
        if translation.LANGUAGE_SESSION_KEY in request.session:
            del request.session[translation.LANGUAGE_SESSION_KEY]
        translation.activate(request.GET.get('lang'))
        request.session[translation.LANGUAGE_SESSION_KEY] = request.GET.get('lang')
        return HttpResponseRedirect(request.GET.get('next'))
    else:
        return reverse('home')


def sendmail(request):
    if request.is_ajax():
        subject = request.GET.get('subject', None)
        content = request.GET.get('content', None)
        header = "Client : %s %s \nMail : %s\nPhone : %s\n\n" % (request.user.first_name, request.user.last_name,
                                                                 request.user.email, request.user.telephone)
        send_mail_smtp(subject, request.user.accountant.email, request.user.email, header + content, None, None)
        data = {'result': True}
        return JsonResponse(data)


urlpatterns = [
    path('', home, name='home'),
    path('confirmation/', comment_creation, name='comment_creation'),
    path('sendmail/', sendmail, name='sendmail'),
    path('agenda/', include('agenda.urls', namespace='agenda')),
    path('customuser/', include('customuser.urls', namespace='customuser')),
    path('company/', include('company.urls', namespace='company')),
    path('simulation/', include('simulation.urls', namespace='simulation')),
    path('lang/', set_language, name='lang'),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('accounts/login/', CustomUserLoginView.as_view(), name='login'),
    path('accounts/update/', check_lang(CustomUserUpdateView.as_view()), name='update_user'),
    path('accounts/password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('hijack/', include('hijack.urls', namespace='hijack')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))]
if not settings.DEBUG:
    handler400 = 'lg.views.bad_request'
    handler403 = 'lg.views.permission_denied'
    handler404 = 'lg.views.page_not_found'
    handler500 = 'lg.views.server_error'
