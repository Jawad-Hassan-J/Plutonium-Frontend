from django.db import models

# Create your models here.

class Tool(models.Model):
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True)
    examples = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name