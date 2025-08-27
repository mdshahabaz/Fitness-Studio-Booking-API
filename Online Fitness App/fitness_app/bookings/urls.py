from django.urls import path
from .views import BookingView, FitnessClassesView, InstructorView

urlpatterns = [
    path('bookings/get-all-bookings/', BookingView.as_view(), name='get-all-bookings'), # get all bookings endpoint
    path('bookings/create-booking/', BookingView.as_view(), name='create-booking'), # create booking endpoint 
    path('classes/get-all-classes/', FitnessClassesView.as_view(), name='get-all-classes'), # get all classes endpoint
    path('classes/create-class/', FitnessClassesView.as_view(), name='create-class'), # create class endpoint
    path('instructors/create-instructor/', InstructorView.as_view(), name='create-instructor'), # create instructor endpoint
]