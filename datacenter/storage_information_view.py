from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone
from datacenter.models import get_duration, format_duration, is_visit_long


def storage_information_view(request):
    non_closed_visits = []
    visit_persons = Visit.objects.filter(leaved_at=None)
    for person in visit_persons:
        visit_long = is_visit_long(person)
        duration = get_duration(person)
        time = format_duration(duration)
        visit_person = (
            timezone.localtime(person.entered_at).strftime(
                "%d %B %Y г. %H:%M:%S"
            )
        )
        visited_people = {
            'who_entered': f'{person.passcard}',
            'entered_at': f'{visit_person}',
            'duration':   f'{time}',
            'is_strange': f'{visit_long}'


        }
        non_closed_visits.append(visited_people)
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
