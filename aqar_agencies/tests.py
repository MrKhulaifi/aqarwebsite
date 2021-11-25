from django.test import TestCase
from django.contrib.auth.models import User
from .models import Agency


class AgencyTestCase(TestCase):

    def test_create_new_agency(self):
        user = User.objects.create(username="alkhulaifi")

        agency = Agency.objects.create(name = "Maktab")

        self.assertEqual(agency.name, "Maktab")
