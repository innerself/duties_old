import calendar
import datetime
from collections import namedtuple
from typing import List

from colorfield.fields import ColorField
from django.db import models
from pytils.translit import slugify


class DutyDate(models.Model):
    date = models.DateField(unique=True)

    def __str__(self) -> str:
        return str(self.date)


class Group(models.Model):
    long_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)

    class Meta:
        ordering = ['long_name']

    def __str__(self) -> str:
        return self.long_name


class DutyPerson(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    local_phone = models.CharField(max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(max_length=50, null=True, blank=True)
    color = ColorField(default='#762f96', unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    duties = models.ManyToManyField(DutyDate)

    class Meta:
        ordering = ['last_name']

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def name_slug(self) -> str:
        return slugify(self.full_name)


class DutyCalendar:
    def __init__(self, year, duty_dates, group):
        self._year = year
        self._calendar = calendar.Calendar().yeardayscalendar(year)
        self._duty_dates = duty_dates
        self._group = group

    def __str__(self):
        return f'{self._year} ({self._group})'

    @property
    def weekheader(self) -> List[str]:
        return calendar.weekheader(3).split()

    @property
    def year(self) -> int:
        return self._year

    @property
    def month_name(self) -> List[str]:
        return calendar.month_name

    @property
    def calendar(self) -> List[List[List[DutyDate]]]:
        return [
            self._fill_month(month_days, month_num)
            for month_num, month_days in enumerate(self._flat_calendar(), 1)
        ]

    def _flat_calendar(self):
        return [
            month
            for quarter in self._calendar
            for month in quarter
        ]

    def _fill_month(self, month_days: List[List[int]], month_num: int):
        return [
            self._fill_week(week, month_num)
            for week
            in month_days
        ]

    def _fill_week(self, week: List[int], month_num: int):
        filled_week = []
        for day in week:
            if day == 0:
                filled_week.append(None)
                continue

            dt = datetime.date(self._year, month_num, day)
            duty = self._duty_dates.filter(
                date=dt,
                dutyperson__group__short_name=self._group,
            ).first()

            DutyInfo = namedtuple('DutyInfo', "date, person")

            if duty:
                person = getattr(duty.dutyperson_set, 'first', None)()
                filled_week.append(DutyInfo(date=dt, person=person))
            else:
                filled_week.append(DutyInfo(date=dt, person=None))

        return filled_week
