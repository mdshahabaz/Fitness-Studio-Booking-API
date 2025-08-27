from django.db import models

class ClassType(models.TextChoices):
    """
    Enumeration of available fitness class types.

    Options:
        YOGA  :  Represents Yoga classes.
        ZUMBA :  Represents Zumba classes.
        HIIT  :  Represents High-Intensity Interval Training classes.
    """
    YOGA = "YOGA", "Yoga"
    ZUMBA = "ZUMBA", "Zumba"
    HIIT = "HIIT", "HIIT"