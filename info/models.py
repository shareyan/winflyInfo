from django.db import models

# Create your models here.

class downloadCount(models.Model):
	count = models.IntegerField(default=0)
