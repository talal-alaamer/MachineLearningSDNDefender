from django.db import models

# Create your models here.
class CaptureLog(models.Model):
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=255)

    class Meta:
        db_table = 'CaptureLog'