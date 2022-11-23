from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration, format_duration, is_visit_long
from django.utils import timezone
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    this_passcard_visits = []
    passcard_visits = Visit.objects.filter(passcard=passcard)
    for visit in passcard_visits:
        duration = get_duration(visit)
        time = format_duration(duration)
        visit_person = (
            timezone.localtime(visit.entered_at).strftime(
                '%d %B %Y г. %H:%M:%S'
            )
        )
        visit_long = is_visit_long(visit)
        visited_people = {
            'entered_at': f'{visit_person}',
            'duration': f'{time}',
            'is_strange': f'{visit_long}'
        }
        this_passcard_visits .append(visited_people)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
