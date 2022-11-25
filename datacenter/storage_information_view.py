from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone
from datacenter.models import get_duration, format_duration, is_visit_long


def storage_information_view(request):
    non_closed_visits = []
    serialized = Visit.objects.filter(leaved_at=None)
    for visit in serialized:
        visit_long = is_visit_long(visit)
        duration = get_duration(visit)
        time = format_duration(duration)
        visit_ = (
            timezone.localtime(visit.entered_at).strftime(
                "%d %B %Y г. %H:%M:%S"
            )
        )
        visited = {
            'who_entered': visit.passcard,
            'entered_at': visit_,
            'duration': time,
            'is_strange': visit_long


        }
        non_closed_visits.append(visited)
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
