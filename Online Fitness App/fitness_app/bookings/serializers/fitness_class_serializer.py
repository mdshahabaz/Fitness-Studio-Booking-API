from django.utils import timezone
from rest_framework import serializers
from bookings.models import ClassType, Instructor
from bookings.serializers.instructor_serializer import InstructorSerializer
from bookings.models.fitness_class_model import FitnessClass

class FitnessClassSerializer(serializers.Serializer):
    """
    Serializer for displaying FitnessClass details.

    Fields:
        id (int): ID of the fitness class (read-only).
        class_name (str): Name/type of the class, must be one of ClassType choices.
        instructor (InstructorSerializer): Nested instructor details.
        available_slots (int): Number of available slots for the class, must be >= 1.
        scheduled_at (datetime): Scheduled date and time of the class.
    
    Validations:
        - Instructor must exist.
        - Scheduled time must be in the future.
    """
    id = serializers.IntegerField(read_only=True)
    class_name = serializers.ChoiceField(choices=ClassType.choices)
    instructor = InstructorSerializer()
    available_slots = serializers.IntegerField(min_value=1)
    scheduled_at = serializers.DateTimeField()

    def validate_instructor_id(self, value):
        try:
            instructor = Instructor.objects.filter(id=value)
        except Instructor.DoesNotExist:
            raise serializers.ValidationError(f"Instructor with {value} does not exist!")
        return value
    
    def validate_scheduled_at(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Scheduled time must be in future!")
        return value
    
class CreateFitnessClassSerializer(serializers.Serializer):
    """
    Serializer for creating a new FitnessClass.

    Fields:
        class_name (str): Name/type of the class, must be one of ClassType choices.
        instructor_id (int): ID of the instructor for the class.
        available_slots (int): Number of available slots for the class, must be >= 1 and <= 100 (to avoid overbooking)
        scheduled_at (datetime): Scheduled date and time of the class.
    
    Validations:
        - Duplicate class checks.
        - Instructor with given ID must exist.
        - Scheduled time must be in the future.
    """
    class_name = serializers.ChoiceField(choices=ClassType.choices)
    instructor_id = serializers.IntegerField()
    available_slots = serializers.IntegerField(min_value=1, max_value=100)
    scheduled_at = serializers.DateTimeField()

    def validate(self, value):
        if FitnessClass.objects.filter(
            class_name=value['class_name'], 
            scheduled_at=value['scheduled_at']
        ).exists():
            raise serializers.ValidationError(
                "A class of this type is already scheduled at this time.")
        return value

    def validate_instructor_id(self, value):
        from ..models import Instructor
        try:
            Instructor.objects.get(id=value)
        except Instructor.DoesNotExist:
            raise serializers.ValidationError("Instructor with this ID does not exist.")
        return value

    def validate_scheduled_at(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Scheduled time must be in the future.")
        return value