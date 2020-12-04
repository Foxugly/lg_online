from django.template.loader import render_to_string
from company.models import Company
from config_process import *
from customuser.models import CustomUser
from tools.mail import send_mail_smtp
from django.utils import timezone


def my_scheduled_test():
    for c in Company.objects.filter(
            subscription_status='2', subscription_date=timezone.now().date()):
        c.subscription_date = timezone.now() + time_to_complete_subscription
        c.save()
        user = CustomUser.objects.filter(companies__id=c.pk)[0]
        dict_context = {'company': c, 'user': user, 'domain': domain, }
        msg_html = render_to_string('mail/step3_uncompleted_dossier.html', dict_context)
        msg_txt = render_to_string('mail/step3_uncompleted_dossier.txt', dict_context)
        subject = '%s %s' % (tag, subject_step3)
        send_mail_smtp(subject, c.accountant.email, reply_to, msg_txt, msg_html, None)
        if show_msg:
            print(msg_txt)
