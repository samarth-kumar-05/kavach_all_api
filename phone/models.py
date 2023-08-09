from django.db import models

# Create your models here.
class PhoneNumber(models.Model):
    phone_number = models.IntegerField()
    carrier = models.CharField(max_length=200)
    phone_region = models.CharField(max_length=250)
    spam_mark = models.IntegerField()
    ham_mark = models.IntegerField()

    def __str__(self):
        return self.phone_number