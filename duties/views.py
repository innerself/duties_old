from decouple import config, Csv
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from duties.models import DutyCalendar


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

        # if user is not None and user.is_staff:
        if user is not None:
            login(request, user)
            return redirect('duties:index')
        else:
            context['access_denied'] = True

    return render(request, 'duties/auth.html', context)


def calendar(request):
    display_years = [
        int(year)
        for year
        in config('CALENDAR_DISPLAY_YEARS', cast=Csv())
    ]

    context = {
        'years': [DutyCalendar(year) for year in display_years],
    }

    return render(request, 'duties/calendar.html', context)


def index(request):
    if request.user.is_anonymous:
        return redirect('duties:auth')
    else:
        return redirect('duties:calendar')
