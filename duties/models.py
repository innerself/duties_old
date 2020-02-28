from django.db import models


class Duty(models.Model):
    start_date = models.DateTimeField
    end_date = models.DateTimeField


class Person(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    local_phone = models.CharField(max_length=64)
    mobile_phone = models.CharField(max_length=64)
    duties = models.ForeignKey(
        Duty,
        on_delete=models.CASCADE,
        related_name='person',
    )

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
