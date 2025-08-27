from bookings.models.booking_model import Booking
from bookings.models.client_model import Client
from bookings.models.fitness_class_model import FitnessClass


class BookingService:
    """
    Service Layer for Booking.

    Funcationalities: 
        1. get_all_bookings() method - for fetching all bookings with respect to email provided
            Input: User/Client email
            Output: Bookings related to user
        2. create_booking() method - for creating a booking with parameters class_id, first_name, last_name and client email
            Input: class_id, first_name, last_name and client_email
            Output: Created booking data
    """
    @staticmethod
    def get_all_bookings(client_email : str):
        try:
            # check if client exists with the email provided
            client = Client.objects.get(email_address=client_email)
        except Client.DoesNotExist:
            return None
        # get all the bookings with respect to the email provided
        bookings = Booking.objects.filter(client=client).select_related(
            'fitness_class', 'fitness_class__instructor'
        )
        return bookings
    
    @staticmethod
    def create_booking(class_id : int, first_name: str, last_name: str, client_email : str):
        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            return None

        # check if slots available
        if fitness_class.available_slots <= 0:
            return None

        # get or create client
        client, _ = Client.objects.get_or_create(
            email_address=client_email,
            defaults={"first_name": first_name, "last_name": last_name}
        )

        # create booking
        booking = Booking.objects.create(
            client=client,
            fitness_class=fitness_class
        )

        # reduce available slots
        fitness_class.available_slots -= 1
        fitness_class.save()

        return booking