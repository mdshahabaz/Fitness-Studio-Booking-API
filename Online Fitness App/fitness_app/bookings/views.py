import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.instructor_service import InstructorService
from .serializers.instructor_serializer import InstructorSerializer
from .services.booking_service import BookingService
from .serializers.booking_serializer import BookingSerializer, CreateBookingSerializer
from .serializers.fitness_class_serializer import FitnessClassSerializer, CreateFitnessClassSerializer
from .services.fitness_class_service import FitnessClassService

# get a logger instance
logger = logging.getLogger(__name__)

class BookingView(APIView):
    """
    API View for handling operations related to Bookings.
    Supports retrieving a client's bookings via email,
    Creates booking provided class id, first name, last name and email 
    """
    def get(self, request):
        """
        Retrieve all bookings associated with a given client email.
        Query Parameters:
            email_address (str): The email address of the client.
        Returns:
            Response: A JSON response containing the list of bookings or an error message. 
        Raises:
            HTTP_400_BAD_REQUEST: If the 'email_address' parameter is missing or no bookings are found.
        """
        client_email = request.query_params.get('email_address')
        logger.info(f"Received email from the params: {client_email}")
        if not client_email:
            logger.error(f"Email is absent in the params!")
            return Response({
                "message": "Email is absent in the params!",
                "status": False,
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)


        all_bookings = BookingService.get_all_bookings(client_email)
        if all_bookings is None:
            logger.error(f"No bookings found for the client email: {client_email}")
            return Response({
                "message": f"No booking exists with email: {client_email}",
                "status": False,
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BookingSerializer(all_bookings, many=True)
        logger.info(f"Successfully fetched all bookings of client: {serializer.data}")
        return Response({
            "message": "Success",
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Create a booking provided with class id, first name, last name and client email
        Request Parameters:
            class_id (int) : ID of the class to be booked.
            first_name (str) : first name of the client.
            last_name (str) : last name of the client.
            email_address (str) : Email address of the client.
        Returns:
            A JSON body with details of the booking created.
        Raises:
            HTTP_400_BAD_REQUEST : if the class is full or any invalid data is provided
            HTTP_500_INTERNAL_SERVER_ERROR : Any other errors caused due to external factors
        """
        serializer = CreateBookingSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Error occured while validating the data: {serializer.errors}")
            return Response({
                "message": "Invalid booking data.",
                "status": False,
                "errors": serializer.errors,
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = BookingService.create_booking(
                serializer.validated_data['class_id'],
                serializer.validated_data['first_name'],
                serializer.validated_data['last_name'],
                serializer.validated_data['email_address'],
            )
            if not booking:
                logger.error(f"Error occured while creating the booking: {serializer.errors}")
                return Response({
                    "message": "Booking failed. Class might be full or invalid data provided.",
                    "status": False,
                    "errors": serializer.errors,
                    "data": []
                }, status=status.HTTP_400_BAD_REQUEST)
            logger.info(f"Successfully created booking for client - {serializer.validated_data['email_address']}, data: {BookingSerializer(booking).data}")
            return Response({
                "message": "Booking created successfully.",
                "status": True,
                "data": BookingSerializer(booking).data
            }, status=status.HTTP_201_CREATED)

        except Exception as error:
            logger.error(f"Exception occured: {error}")
            return Response({
                "message": f"Something went wrong: {str(error)}",
                "status": False,
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class FitnessClassesView(APIView):
    """
    APIView for handling operations supported by Fitness Classes.
    Supports getting all fitness classes
    Creates class according to the requirements
    """
    def get(self, request):
        """
        Retrieves all the upcoming classes
        Returns:
            A JSON body with all the upcoming classes data if present, else an empty array object
        """
        logger.info("Getting all classes")
        all_fitness_classes = FitnessClassService.get_all_classes()

        serializer = FitnessClassSerializer(all_fitness_classes, many=True)
        logger.info("Fetched all upcoming classes successfully!")
        return Response({
            "message": "Fetched all upcoming classes successfully!",
            "status":True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Creates a fitness class provided with class name, instructor id, available slots and scheduled time
        Request Parameters:
            class_name(str : choices) : Choices of YOGA, ZUMBA, HIIT
            instructor_id (int): ID of the instructor associated with the class
            available_slots (int): Number of slots open for the class
            scheduled_at (datetimefield) : timestamp for the class associated
        Returns:
            A JSON body containing newly created fitness class details.
        Raises:
            HTTP_400_BAD_REQUEST: for any data invalidations
        """
        serializer = CreateFitnessClassSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Error occured while validating data: {serializer.errors}")
            return Response({
                "message": "Invalid data",
                "status": False,
                "errors": serializer.errors,
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            logger.info("Creating class with provided data...")
            fitness_class = FitnessClassService.create_fitness_class(
                data['class_name'],
                data['instructor_id'],
                data['available_slots'],
                data['scheduled_at']
            )

            logger.info(f"Created class successfully with details: {FitnessClassSerializer(fitness_class).data}")
            return Response({
                "message": "Fitness class created successfully!",
                "status": True,
                "data": FitnessClassSerializer(fitness_class).data
            }, status=status.HTTP_201_CREATED)
        except Exception as error:
            logger.error(f"Exception occured: {error}")
            return Response({
                "message": str(error),
                "status": False,
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

class InstructorView(APIView):
    """
    APIView for handling operations supporting Instructors.
    Supports creating instructor provided with data
    """
    def post(self, request):
        """
        Creates an instructor object provided with instructor name parameter.
        Request parameters: 
            instructor_name (str): Name of the instructor to be created
        Returns:
            A JSON body containing newly created instructor object
        Raises:
            HTTP_400_BAD_REQUEST : if any data invalidations.
        """
        name = request.data.get("instructor_name")
        logger.info(f"Received instructor name for creating instructor: {name}")
        if not name:
            logger.error("Instructor name is not provided")
            return Response({
                "message": "Instructor name is required",
                "status": False,
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        instructor = InstructorService.create_instructor(name)
        logger.info(f"Successfully created instructor object with data: {InstructorSerializer(instructor).data}")
        return Response({
            "message": "Instructor created successfully",
            "status": True,
            "data": InstructorSerializer(instructor).data
        }, status=status.HTTP_201_CREATED)