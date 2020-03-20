import datetime

from django.shortcuts import render

from duties.models import DutyDate


def index(request):
    today = datetime.date.today()
    duties_today = DutyDate.objects.filter(date=today).first().dutyperson_set.all()
    context = {
        'duty': duties_today,
        'groups': [person.group for person in duties_today]
    }

    return render(request, 'duties/index.html', context)
