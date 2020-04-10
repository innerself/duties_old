from decouple import config, Csv
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from duties.models import DutyCalendar, DutyPerson, DutyDate


def auth(request, action='login'):
    if action == 'logout':
        logout(request)
        return redirect('duties:auth')

    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
        'login': {
            'prefix': config('LOGIN_PREFIX', default='DOMAIN\\'),
            'placeholder': config('LOGIN_PLACEHOLDER', default='Login'),
        },
        'access_denied': False,
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request=request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect('duties:index')
        else:
            context['access_denied'] = True

    return render(request, 'duties/auth.html', context)


# TODO why redirects through / despite ?next=... presence?
@login_required
def calendar(request, group):
    display_years = [
        int(year)
        for year
        in config('CALENDAR_DISPLAY_YEARS', cast=Csv())
    ]

    duty_dates = DutyDate.objects.filter(
        date__year__gte=min(display_years),
        date__year__lte=max(display_years),
    )

    context = {
        'calendar': [
            DutyCalendar(year, duty_dates, group)
            for year
            in display_years
        ],
        'group': group,
        'duty_persons': DutyPerson.objects.filter(group__short_name=group),
    }

    return render(request, 'duties/calendar.html', context)


def index(request):
    if request.user.is_anonymous:
        return redirect('duties:auth')
    else:
        return redirect('duties:calendar')
