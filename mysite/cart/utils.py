from datetime import timedelta
from django.utils import timezone


def default_date_order():
    return timezone.now() + timedelta(days=1)
