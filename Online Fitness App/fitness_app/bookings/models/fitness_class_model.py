from django.db import models
from bookings.models.class_type_choices import ClassType
from bookings.models.instructor_model import Instructor

class FitnessClass(models.Model):
    """
    Represents a fitness class offered in the studio.

    Attributes:
        class_name (str): The type of class (Yoga, Zumba, HIIT), chosen from `ClassType`.
        instructor (Instructor): The instructor conducting the class.
        available_slots (int): Number of available booking slots for the class.
        created_date (datetime): The timestamp when the class was created.
        updated_on (datetime): The timestamp when the class details were last updated.
        scheduled_at (datetime): The scheduled date and time for the class. 
    """
    class_name = models.CharField(max_length=100, choices=ClassType.choices)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    available_slots = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    scheduled_at = models.DateTimeField()

    def __str__(self):
        """Return a human-readable string representation of the fitness classes."""
        return f"{self.class_name} by {self.instructor.instructor_name} at {self.scheduled_at}" 