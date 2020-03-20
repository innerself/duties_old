import datetime

from django.db import models


class DutyDate(models.Model):
    date = models.DateField()

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
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    duties = models.ManyToManyField(DutyDate)

    class Meta:
        ordering = ['last_name']

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
