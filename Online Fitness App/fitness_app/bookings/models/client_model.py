from django.db import models

class Client(models.Model):
    """
    Represents Client (user) model.

    Attributes:
        first_name(str) :  First name of the client
        last_name(str)  : Last name of the client
        email_address(str): Email address of the client
        phone_number(str) : Phone number of the client
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        """Return a human-readable string representation of the client."""
        return f"{self.first_name} | {self.last_name}"