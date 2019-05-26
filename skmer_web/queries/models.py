from django.db import models


# Create your models here.
class Query(models.Model):
    fileName = models.FileField()

