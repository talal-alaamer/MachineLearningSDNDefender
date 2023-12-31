from django.db import models
from djongo import models as djongo_models
from django.utils import timezone

# Create your models here.
class AuditLog(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    username = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'audit_log'