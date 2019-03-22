from django.utils import timezone
from datetime import timedelta


def add_90_days():
    return timezone.now() + timedelta(days=90)


def minus_10_second_buffer():
    return timezone.now() - timedelta(seconds=10)
