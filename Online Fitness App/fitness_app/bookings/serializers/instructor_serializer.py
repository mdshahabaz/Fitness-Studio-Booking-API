from rest_framework import serializers

class InstructorSerializer(serializers.Serializer):
    """
    Serializer for Instructor model.

    Fields:
        id (int): ID of the instructor (read-only).
        instructor_name (str): Name of the instructor, max length 100.

    Validations:
        - instructor_name cannot be empty or whitespace.
        - instructor_name length must not exceed 100 characters.
    """
    id = serializers.IntegerField(read_only=True)
    instructor_name = serializers.CharField(max_length=100)

    def validate_instructor_name(self, value):
        """
        Ensure the instructor name is not empty or just whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError("Instructor name cannot be empty or whitespace.")
        return value