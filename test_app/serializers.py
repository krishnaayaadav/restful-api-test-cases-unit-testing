from rest_framework import serializers
from .models import Puppies

class PuppiesSerializer(serializers.ModelSerializer):
   
   class Meta:
      model  = Puppies
      fields = ('id', 'name', 'age', 'breed', 'color', 'created_at')