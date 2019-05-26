from django.db import models

class RefFile(models.Model):
    reference_name = models.TextField(max_length=50)
    file = models.FileField(upload_to='reference_lib/', blank=True, null=True)
