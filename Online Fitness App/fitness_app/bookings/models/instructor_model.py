from django.db import models

class Instructor(models.Model):
    """
    Represents Instructor who will be taking classes

    Attributes:
        instructor_name(str) : Name of the instructor
    """
    instructor_name = models.CharField(max_length=100)

    def __str__(self):
        """Return a human-readable string representation of the instructor."""
        return f"{self.instructor_name}"