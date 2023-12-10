from django.db import models

# Create your models here.
class WalletAddress(models.Model):
    address = models.CharField(max_length=100)
    spam_marks = models.IntegerField()

    def __str__(self):
        return self.address