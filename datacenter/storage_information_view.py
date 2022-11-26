from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone
from datacenter.models import get_duration, format_duration, is_visit_long


def storage_information_view(request):
    non_closed_visits = []
    visits = Visit.objects.filter(leaved_at=None)
    for visit in visits:
        visit_long = is_visit_long(visit)
        duration = get_duration(visit)
        formatted_duration = format_duration(duration)
        formatted_entered_at = (
            timezone.localtime(visit.entered_at).strftime(
                "%d %B %Y г. %H:%M:%S"
            )
        )
        serialized_visit = {
            'who_entered': visit.passcard,
            'entered_at': formatted_entered_at,
            'duration': formatted_duration,
            'is_strange': visit_long


        }
        non_closed_visits.append(serialized_visit)
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
