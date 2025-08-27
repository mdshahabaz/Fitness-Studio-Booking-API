from bookings.models.fitness_class_model import FitnessClass
from bookings.models.instructor_model import Instructor
from django.utils.timezone import now

class FitnessClassService:
    """
    Service layer for Fitness class

    Functionalities:
        1. get_all_classes() - fetches all upcoming classes
            Input: None
            Output: All classes whose scheduled at time is greater than the current time and orderd by time the class is scheduled

        2. create_fitness_class() - creates a fitness class with parameters: class_name, instructor_id, available_slots and scheduled_at time
            Input: class_name, instructor_id, available_slots and scheduled_at time
            Output: Fitness class created
    """

    @staticmethod
    def get_all_classes():
        try:
            classes = FitnessClass.objects.filter(scheduled_at__gte=now()).select_related('instructor').order_by('scheduled_at')
        except FitnessClass.DoesNotExist:
            return None
        return classes
        

    @staticmethod
    def create_fitness_class(class_name, instructor_id, available_slots, scheduled_at):
        return FitnessClass.objects.create(
            class_name=class_name,
            instructor_id=instructor_id,
            available_slots=available_slots,
            scheduled_at=scheduled_at
        )