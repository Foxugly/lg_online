from django.utils import timezone
from company.models import Company


def my_scheduled_test():
    c = Company.objects.filter(subscription_status=2)

    c.subscription_date = timezone.now()
    c.save()


