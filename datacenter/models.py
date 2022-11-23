from django.db import models
from django.utils import timezone
import datetime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit):
    entered_time = timezone.localtime(visit.entered_at)
    leaved_at = timezone.localtime(visit.leaved_at)
    if not visit.leaved_at:
        todey_time = timezone.localtime()
        duration = todey_time - entered_time
        return duration
    duration = leaved_at - entered_time
    return duration


def format_duration(duration):
    time = str(duration)[0:7]
    return time


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    return duration > datetime.timedelta(minutes=minutes)
