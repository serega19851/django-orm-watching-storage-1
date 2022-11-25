from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration, is_visit_long
from django.utils import timezone
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    passcard_visits = []
    serialized = Visit.objects.filter(passcard=passcard)
    for visit in serialized:
        duration = get_duration(visit)
        time = format_duration(duration)
        visit_ = (
            timezone.localtime(visit.entered_at).strftime(
                '%d %B %Y г. %H:%M:%S'
            )
        )
        visit_long = is_visit_long(visit)
        visited = {
            'entered_at': visit_,
            'duration': time,
            'is_strange': visit_long
        }
        passcard_visits .append(visited)
    context = {
        'passcard': passcard,
        'this_passcard_visits': passcard_visits
    }
    return render(request, 'passcard_info.html', context)
