from django.core.management.base import BaseCommand
from django.utils import timezone
from bookings.models.instructor_model import Instructor
from bookings.models.fitness_class_model import FitnessClass
from bookings.models.booking_model import Booking
from bookings.models.client_model import Client
import pytz

class Command(BaseCommand):
    help = "Seed instructors, clients, fitness classes, and bookings (wipe existing data)."

    def handle(self, *args, **kwargs):
        ist = pytz.timezone("Asia/Kolkata")

        # clear existing data
        Booking.objects.all().delete()
        FitnessClass.objects.all().delete()
        Instructor.objects.all().delete()
        Client.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared all existing data!"))

        # seed instructors
        instructors_data = [
            {"id": 1, "instructor_name": "John Doe"},
            {"id": 2, "instructor_name": "Jane Smith"},
            {"id": 3, "instructor_name": "Michael Johnson"},
        ]

        instructors = {}
        for data in instructors_data:
            instructor = Instructor.objects.create(
                id=data["id"], instructor_name=data["instructor_name"]
            )
            instructors[data["id"]] = instructor
            self.stdout.write(self.style.SUCCESS(f"Instructor '{data['instructor_name']}' created"))

        #seed fitness class data
        classes_data = [
            {
                "class_name": "YOGA",
                "instructor_id": 1,
                "available_slots": 10,
                "scheduled_at": timezone.datetime(2025, 9, 1, 7, 0, 0)
            },
            {
                "class_name": "ZUMBA",
                "instructor_id": 2,
                "available_slots": 15,
                "scheduled_at": timezone.datetime(2025, 8, 30, 10, 30, 0)
            },
            {
                "class_name": "HIIT",
                "instructor_id": 3,
                "available_slots": 5,
                "scheduled_at": timezone.datetime(2025, 9, 3, 6, 30, 0)
            },
        ]

        fitness_classes = {}
        for c in classes_data:
            scheduled_time = ist.localize(c["scheduled_at"])
            fc = FitnessClass.objects.create(
                class_name=c["class_name"],
                instructor=instructors[c["instructor_id"]],
                available_slots=c["available_slots"],
                scheduled_at=scheduled_time
            )
            fitness_classes[c["class_name"]] = fc
            self.stdout.write(self.style.SUCCESS(f"Fitness Class '{c['class_name']}' created"))

        # seed clients data
        clients_data = [
            {"first_name": "Alice", "last_name": "Wonderland", "email_address": "alice@example.com", "phone_number": "9999999999"},
            {"first_name": "Bob", "last_name": "Marley", "email_address": "bob@example.com", "phone_number": "8888888888"},
            {"first_name": "Anne", "last_name": "Gold", "email_address": "anne.gold@gmail.com", "phone_number": "7777777777"},
        ]

        clients = {}
        for c in clients_data:
            client = Client.objects.create(
                first_name=c["first_name"],
                last_name=c["last_name"],
                email_address=c["email_address"],
                phone_number=c["phone_number"]
            )
            clients[c["email_address"]] = client
            self.stdout.write(self.style.SUCCESS(f"Client '{c['first_name']}' created"))

        # seed bookings
        bookings_data = [
            {"client_email": "alice@example.com", "class_name": "YOGA"},
            {"client_email": "bob@example.com", "class_name": "ZUMBA"},
            {"client_email": "anne.gold@gmail.com", "class_name": "ZUMBA"},
        ]

        for b in bookings_data:
            client = clients[b["client_email"]]
            fc = fitness_classes[b["class_name"]]
            Booking.objects.create(
                client=client,
                fitness_class=fc
            )
            # decrement available slots
            fc.available_slots -= 1
            fc.save()
            self.stdout.write(self.style.SUCCESS(f"Booking for {client.first_name} in {fc.class_name} created"))

        self.stdout.write(self.style.SUCCESS("Seed data completed successfully!"))
