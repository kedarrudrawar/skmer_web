from django.db import models


# Create your models here.
class Query(models.Model):
    fileName = models.CharField(max_length=100)
    queryFile = models.FileField(upload_to='queryFiles/', null=True, blank=True)

    def __str__(self):
        return self.fileName

