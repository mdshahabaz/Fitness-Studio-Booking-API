from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from bookings.models.instructor_model import Instructor
from bookings.models.fitness_class_model import FitnessClass
from django.utils.timezone import now, timedelta

class FitnessAPIUnitTests(TestCase):
    # Initial setup
    def setUp(self):
        self.client = APIClient()
        self.instructor = Instructor.objects.create(instructor_name="Alice")
        self.fclass = FitnessClass.objects.create(
            class_name="YOGA",
            instructor=self.instructor,
            available_slots=2,
            scheduled_at=now() + timedelta(days=1)
        )

    # Test GET /classes
    def test_get_classes(self):
        response = self.client.get("/api/classes/get-all-classes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["class_name"], "YOGA")

    # Test successful POST /book
    def test_create_booking_success(self):
        payload = {
            "class_id": self.fclass.id,
            "first_name": "John",
            "last_name": "Doe",
            "email_address": "john@example.com"
        }
        response = self.client.post("/api/bookings/create-booking/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["status"])
        # Slots should decrease
        self.fclass.refresh_from_db()
        self.assertEqual(self.fclass.available_slots, 1)

    # Test POST /book when slots are full
    def test_create_booking_full_class(self):
        self.fclass.available_slots = 0
        self.fclass.save()
        payload = {
            "class_id": self.fclass.id,
            "first_name": "Jane",
            "last_name": "Doe",
            "email_address": "jane@example.com"
        }
        response = self.client.post("/api/bookings/create-booking/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["status"])

    # Test GET /bookings by email
    def test_get_bookings_by_email(self):
        # First create a booking
        payload = {
            "class_id": self.fclass.id,
            "first_name": "John",
            "last_name": "Doe",
            "email_address": "john@example.com"
        }
        self.client.post("/api/bookings/create-booking/", payload, format="json")
        # Now fetch bookings
        response = self.client.get("/api/bookings/get-all-bookings/?email_address=john@example.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["email_address"], "john@example.com")
