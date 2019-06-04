from django.db import models
from django.template.defaultfilters import mark_safe


# Create your models here.
class Queries(models.Model):
    collection_name = models.CharField(max_length=100)

    def __str__(self):
        return self.collection_name


class Query(models.Model):
    fileName = models.CharField(max_length=100, default='query')
    queryFile = models.FileField(upload_to='queryFiles/', null=True, blank=True)
    query_collection = models.ForeignKey(Queries, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.fileName
