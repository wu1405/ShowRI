from django.db import models

# Create your models here.
class Reserved_tmp(models.Model):
	region = models.CharField(max_length=20)
	type = models.CharField(max_length=20)
	count = models.IntegerField(max_length=10)
	account = models.CharField(max_length=20)
	duration = models.IntegerField(max_length=10)
	end = models.CharField(max_length=40)

#class Reserved_sum(models.Model):
#	region = models.CharField(max_length=20)
#	type = models.CharField(max_length=20)
#	total = models.IntegerField(max_length=10)

class Reserved_final(models.Model):
	region = models.CharField(max_length=20)
	type = models.CharField(max_length=20)
	used_num = models.IntegerField(max_length=10)
	ri_num = models.IntegerField(max_length=10)
	delta = models.IntegerField(max_length=10)
	account = models.CharField(max_length=20)
		
	
