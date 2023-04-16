from django.db import models


class Company(models.Model):

	name = models.CharField(max_length=150, blank=False, null=False)
	region = models.CharField(max_length=100, blank=False, null=False)
	link = models.URLField()

	def __str__(self):

		return f"${self.name, self.region}"
