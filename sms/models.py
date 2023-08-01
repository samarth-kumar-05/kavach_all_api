from django.db import models

# Create your models here.
class SMSHeaders(models.Model):
    name = models.CharField(max_length=50)
    spam_mark = models.IntegerField()

    def __str__(self):
        return self.name
