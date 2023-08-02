from django.db import models

# Create your models here.
class PhoneNumber(models.Model):
    phone_number = models.IntegerField()
    spam_mark = models.IntegerField()

    def __str__(self):
        return self.phone_number