from django.db import models

# Create your models here.

class Puppies(models.Model):
   name = models.CharField(max_length=255)
   breed = models.CharField(max_length=255)
   color = models.CharField(max_length=255)
   age = models.IntegerField()
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   
   def get_breed(self):
      return f'{self.name} belogns to {self.breed}'
   
   def __repr__(self):
      return self.name + 'is added'
   
   
   