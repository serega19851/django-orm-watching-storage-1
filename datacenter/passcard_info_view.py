from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration, is_visit_long
from django.utils import timezone
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    passcard_visits = []
    visits = Visit.objects.filter(passcard=passcard)
    for visit in visits:
        duration = get_duration(visit)
        formatted_duration = format_duration(duration)
        formatted_entered_at = (
            timezone.localtime(visit.entered_at).strftime(
                '%d %B %Y г. %H:%M:%S'
            )
        )
        visit_long = is_visit_long(visit)
        serialized_visit = {
            'entered_at': formatted_entered_at,
            'duration': formatted_duration,
            'is_strange': visit_long
        }
        passcard_visits .append(serialized_visit)
    context = {
        'passcard': passcard,
        'this_passcard_visits': passcard_visits
    }
    return render(request, 'passcard_info.html', context)
