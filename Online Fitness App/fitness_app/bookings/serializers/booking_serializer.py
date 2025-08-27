from rest_framework import serializers
from bookings.models import FitnessClass
from django.utils import timezone


class BookingSerializer(serializers.Serializer):
    """
    Serializer for booking information.

    Fields:
        first_name (str): First name of the client.
        last_name (str): Last name of the client.
        email_address (str): Email address of the client.
        fitness_class_name (str): Name of the booked fitness class.
        scheduled_at (datetime): Scheduled date and time of the fitness class.
        instructor_name (str): Name of the instructor leading the class.
        booked_at (datetime): Timestamp when the booking was created.
    """
    first_name = serializers.CharField(source='client.first_name', read_only=True)
    last_name = serializers.CharField(source='client.last_name', read_only=True)
    email_address = serializers.EmailField(source='client.email_address', read_only=True)
    fitness_class_name = serializers.CharField(source='fitness_class.class_name', read_only=True)
    scheduled_at = serializers.DateTimeField(source='fitness_class.scheduled_at', read_only=True)
    instructor_name = serializers.CharField(source='fitness_class.instructor.instructor_name', read_only=True)
    booked_at = serializers.DateTimeField(read_only=True)


class CreateBookingSerializer(serializers.Serializer):
    """
    Serializer for creating a new booking request.

    Fields:
        class_id (int): ID of the fitness class to be booked.
        first_name (str): First name of the client.
        last_name (str): Last name of the client.
        email_address (str): Email address of the client.

    Validations:
        - Ensures the fitness class exists.
        - Ensures the class has available slots.
        - Ensures the class is not already scheduled in the past.
        - Ensures email address is unique for the same class.
        - Ensures names are non-empty and alphabetic.
    """
    class_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email_address = serializers.EmailField()

    def validate_class_id(self, value):
        try:
            fitness_class = FitnessClass.objects.get(id=value)
        except FitnessClass.DoesNotExist:
            raise serializers.ValidationError("Fitness class with ID {value} does not exist.")
        
        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No available slots for this class.")
        
        if fitness_class.scheduled_at < timezone.now():
            raise serializers.ValidationError("Cannot book a class that has already started or finished.")
        return value

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        if not value.isalpha():
            raise serializers.ValidationError("First name should contain only letters.")
        return value
    
    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Last name cannot be empty")
        if not value.isalpha():
            raise serializers.ValidationError("Last name should contain only letters.")
        return value
    
    def validate_email_address(self, value):
        class_id = self.initial_data.get("class_id")
        if class_id and FitnessClass.objects.filter(id=class_id, bookings__client__email_address=value).exists():
            raise serializers.ValidationError("This email is already registered for the selected class.")
        return value

