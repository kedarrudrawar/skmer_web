from django.db import models

class RefLibrary(models.Model):
    reference_name = models.CharField(max_length=50)
    file = models.FileField(upload_to='reference_lib/')
