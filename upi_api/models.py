from django.db import models

# Create your models here.
class UPIAddress(models.Model):
    upi_id = models.CharField(max_length=250)
    spam_mark = models.IntegerField()
    ham_mark = models.IntegerField()

    def __str__(self):
        return self.upi_id

