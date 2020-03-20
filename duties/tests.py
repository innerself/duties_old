import datetime

from django.test import TestCase, Client

from .models import DutyDate, Group, DutyPerson
from .utils import generate_duties, generate_groups, generate_persons


class TestView(TestCase):

    def test_view(self):
        client = Client()
        self.assertEquals(client.get('/').status_code, 200)


class TestUtils(TestCase):

    def test_generate_groups(self):
        self.assertFalse(Group.objects.all().exists())
        generate_groups()
        self.assertTrue(Group.objects.all().exists())

    def test_generate_persons(self):
        self.assertRaises(ValueError, generate_persons)

        generate_groups()
        generate_persons(number=10)
        self.assertEqual(len(DutyPerson.objects.all()), 10)

        generate_persons(number=5)
        self.assertEqual(len(DutyPerson.objects.all()), 15)

    def test_generate_duties(self):
        generate_groups()
        generate_persons()

        generate_duties(datetime.date(2020, 1, 1), datetime.date(2020, 1, 5))
        self.assertEquals(len(DutyDate.objects.all()), 5)

        generate_duties(datetime.date(2020, 1, 10), datetime.date(2020, 1, 11))
        self.assertEquals(len(DutyDate.objects.all()), 7)
