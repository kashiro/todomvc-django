from django.db import models

# Create your models here.

class Todo(models.Model):
    '''Todo model'''
    title = models.CharField('title', max_length=255)
    completed = models.BooleanField('completed', default=False)

