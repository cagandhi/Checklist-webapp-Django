from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Checklist(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	visibility = models.IntegerField(default=0)

	def __str__(self):
		return self.title