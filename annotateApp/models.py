from django.db import models

# Create your models here.
# class Photos(models.Model):
#     name = models.CharField(max_length=255)
#     place_id = models.IntegerField()
#     lat = models.CharField(max_length=255)
#     lon = models.CharField(max_length=255)
#     time = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='photos')


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos')


class Data(models.Model):
    place_id = models.IntegerField()
    lat = models.CharField(max_length=255)
    lon = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    image = models.CharField(max_length=255)