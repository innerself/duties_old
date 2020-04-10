import datetime
import random

import mimesis
from .models import DutyPerson, Group, DutyDate


def generate_persons(number: int = 20) -> None:
    person_generator = mimesis.Person('ru')
    text_generator = mimesis.Text()
    all_groups = Group.objects.all()
    if not all_groups:
        raise ValueError('You must create groups before persons')

    print(f'Creating {number} fake persons')

    for _ in range(number):
        DutyPerson.objects.create(
            first_name=person_generator.first_name(),
            last_name=person_generator.last_name(),
            email=person_generator.email(),
            local_phone='-'.join(person_generator.telephone().split('-')[-2:]),
            mobile_phone=person_generator.telephone(),
            color=text_generator.hex_color(safe=True),
            group=random.choice(all_groups),
        )

    return None


def generate_groups() -> None:
    groups_info = {
        'System administration': 'sys_adm',
        'Network administration': 'net_adm',
        'Virtualization': 'virt',
    }

    print(f'Creating {len(groups_info)} fake groups')

    for long_name, short_name in groups_info.items():
        Group.objects.create(
            long_name=long_name,
            short_name=short_name,
        )

    return None


def generate_duties(start_date=None, end_date=None) -> None:
    if not start_date:
        this_year = datetime.date.today().year
        start_date = datetime.date(this_year, 1, 1)

    if not end_date:
        this_year = datetime.date.today().year
        end_date = datetime.date(this_year, 12, 31)

    all_persons = DutyPerson.objects.all()
    if not all_persons:
        raise ValueError('You must create persons before duties')

    print(f'Creating {(end_date - start_date).days} fake duties')

    current_date = start_date
    while current_date <= end_date:
        dd = DutyDate(date=current_date)
        dd.save()
        duty_person = random.choice([*all_persons, None])

        if duty_person:
            duty_person.duties.add(dd)

        current_date += datetime.timedelta(days=1)

    return None


def clear_groups() -> None:
    all_groups = Group.objects.all()
    print(f'Removing {len(all_groups)} groups')
    all_groups.delete()

    return None


def clear_persons() -> None:
    all_persons = DutyPerson.objects.all()
    print(f'Removing {len(all_persons)} persons')
    all_persons.delete()

    return None


def clear_duties() -> None:
    all_duties = DutyDate.objects.all()
    print(f'Removing {len(all_duties)} duties')
    all_duties.delete()


def clear_all() -> None:
    clear_duties()
    clear_persons()
    clear_groups()
