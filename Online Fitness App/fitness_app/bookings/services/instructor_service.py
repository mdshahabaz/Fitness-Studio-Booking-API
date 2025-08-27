from bookings.models.instructor_model import Instructor


class InstructorService:
    @staticmethod
    def create_instructor(name: str) -> Instructor:
        """
        Creates a new instructor if it doesn't exist.
        Returns the Instructor instance.
        """
        instructor, created = Instructor.objects.get_or_create(instructor_name=name)
        return instructor