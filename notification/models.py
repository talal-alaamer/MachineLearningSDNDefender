from django.db import models

# Create your models here.
class Notification(models.Model):
    sha256 = models.CharField(max_length=64)
    date = models.DateField()
    time = models.TimeField()
    title = models.CharField(max_length=200)

    class Meta:
        db_table = 'Notification'