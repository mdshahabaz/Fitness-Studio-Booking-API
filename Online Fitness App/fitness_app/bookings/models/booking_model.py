from django.db import models
from bookings.models.client_model import Client
from bookings.models.fitness_class_model import FitnessClass

class Booking(models.Model):
    """
    Represents a booking made by a client for a specific fitness class.

    Attributes:
        client (ForeignKey): The client who made the booking.
        fitness_class (ForeignKey): The fitness class that was booked.
        booked_at (DateTimeField): Timestamp of when the booking was created.
    """
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="bookings"
        )
    fitness_class = models.ForeignKey(
        FitnessClass, on_delete=models.CASCADE, related_name="bookings"
        )
    booked_at = models.DateTimeField(
        auto_now_add=True
        )

    def __str__(self):
        """Return a human-readable string representation of the booking."""
        return f"{self.client.first_name} booked {self.fitness_class.class_name} at {self.booked_at}"