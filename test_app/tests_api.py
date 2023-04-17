
from django.test import TestCase,Client
from .models import Puppies
from django.urls import reverse
from .serializers import PuppiesSerializer
import json
from rest_framework import status

client = Client()

valid_status = status.HTTP_200_OK
not_found    = status.HTTP_404_NOT_FOUND
valid_insertion = status.HTTP_201_CREATED
bad_request     = status.HTTP_400_BAD_REQUEST


class PuppyTester(TestCase):
   """Test class for  models checking insertion"""
   
   def setUp(self):
      """default set-up here"""
      name = ('Casper', 'Muffin', 'Suffin', 'Caffin')
      age  = (2,4,3,1)
      breeds = ("Bull Dog", "Dasion", 'Others', 'Others')
      color  = ('Black', 'Brown', 'Black', 'Black')
      for i in range(4):
         # creating four object here
         Puppies.objects.create(name=name[i], age=age[i], breed=breeds[i], color=color[i])
         
   def test_is_puppy_created(self):
      """is model obj is created and data insert accuraley or not"""
      name = ('Casper', 'Muffin', 'Suffin', 'Caffin')
      age  = (2,4,3,1)
      color  = ('Black', 'Brown', 'Black', 'Black')
      
      
      for i in range(4):
         nm = name[i]
         ag  = age[i]
         clr = color[i]
         pup_obj = Puppies.objects.get(name=nm)
         
         # checking is age is same or not
         self.assertEqual(pup_obj.age, ag)
         
         # checking name is same or not
         self.assertEqual(pup_obj.name, nm)
         
         # checking color is same or not
         self.assertEqual(pup_obj.color, clr)
         
      print('\n All test cases  of test_is_puppy_created is passed successfuly')
      
   def test_get_all_objs(self):
      """checking no of objs"""
      objs = Puppies.objects.all()
      
      self.assertGreaterEqual(objs.count(), 4)
      
      print('\n yes 4 or more than objs are founded')
   
   def test_all_using_reverse(self):
      # api response
      res = client.get(reverse('get_and_post'))
      print('\n ', res, res.status_code, (res.data))
      
      # our db data
      puppies = Puppies.objects.all()
      
      serializer = PuppiesSerializer(puppies, many=True)
      
      # checking response and db serialized data is equal or not
      self.assertEqual(serializer.data, res.data)
      
      # checking response status code is equal to http 200 response or not
      self.assertEqual(res.status_code, status.HTTP_200_OK )
      
      print('\n Getting all data with 200 ok response')
   
class SingleObjeTester(TestCase):
   """Here we will check two things as 
      1. obj exists than what is response
      2. when not exits than how it responsing
      
      """
   
   def setUp(self):
      # here we create two obj of puppies and storing their refrence
      
      
      self.muffin = Puppies.objects.create(name="Muffin", color='Brown', age=3, breed='Muffin')
      self.bull   = Puppies.objects.create(name='Bull', color='Black', breed='Bull Dog', age=3)
      
      # 
      
   def test_valid_single_obj(self):
      pk = self.muffin.pk
      response = client.get(reverse('update_endpoints', kwargs={'pk': pk}))
      
      print(response, response.status_code,response.data)
      
      try:
         pup = Puppies.objects.get(pk=pk)
      except:
         pass
      else:
         serializer = PuppiesSerializer(pup)
         
         # checking both data 
         self.assertEqual(serializer.data, response.data)
         
         # status code check
         self.assertEqual(response.status_code, valid_status)
         
         print('\n Single object data is valid')
      
      
   def test_not_found_obj(self):
      response = client.get(reverse('update_endpoints', kwargs={'pk': 12}))
      
      self.assertEqual(response.status_code, not_found)
      
class PuppyInsertionTest(TestCase):
   
   def setUp(self):
      
      # here creating valid data for insertion
      self.valid_data = {
         "name": "Muffin",
         "color": "Brown",
         "age": 3, # here age is integer
         "breed": "Muffin"
      }
      
      # invalida data
      self.invalida_data = {
         "name": "Bull",
         "age": "32f",
         "breed": '',
         "color": "Brown"
      }
      
   def test_valid_insertion(self):
      data = json.dumps(self.valid_data)
      response = client.post(reverse('get_and_post'), data=data, content_type='application/json')
      
      self.assertEqual(response.status_code, valid_insertion)
      
      print('\n yes valid insertion is done' )
      
   def test_invalid_insertions(self):
      data = json.dumps(self.invalida_data)
      response = client.post(reverse('get_and_post'), data=data, content_type='application/json')
      
      self.assertEqual(response.status_code, bad_request)
      print('\n no it is in-valid insertion ' )
      
class UpdationTester(TestCase):
   
   def setUp(self):
      
      self.valid_pup = Puppies.objects.create(name='Bull', color="Brown", breed="Bull Dog", age=2)
      
      self.invalid_pup = Puppies.objects.create(name='Muffin', color="Black", breed="Muffin", age=5)
      
      self.valid_data = {
         "name": "Bull Dog",
         "age":  3
      }
      
      self.invalid_data = {
         "name": "",
         "age": '',
         "breed": "Muffins"
      }
      
   
   def test_valid_updation(self):
      pk = self.valid_pup.pk
      data = json.dumps(self.valid_data)
      response = client.patch(reverse('update_endpoints', kwargs={'pk': pk}),data=data, content_type='application/json')
      
      self.assertEqual(response.status_code, valid_status)
      
      print('\n updation test successufly')
      
   def test_invalid_updation(self):
      pk = self.invalid_pup.pk 
      data = json.dumps(self.invalid_data)
      
      response = client.patch(reverse('update_endpoints', kwargs={'pk': pk}), data=data, content_type='application/json')
      
      self.assertEqual(response.status_code, bad_request )
      print('\n invalid tested  successufly')
      
class DeletionTester(TestCase):
   
   def setUp(self):
      self.obj1 = Puppies.objects.create(name='Bull', color="Brown", breed="Bull Dog", age=2)
      
      self.obj2 = Puppies.objects.create(name='Muffin', color="Black", breed="Muffin", age=5)
   
   def test_valid_deletion(self):
      pk = self.obj1.pk 
      
      response = client.delete(reverse('update_endpoints', kwargs={'pk': pk}), content_type='application/json')
      
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      
      print('\n Deletion performed successfuly')
      
   def test_valid_deletion(self):
      pk = 45
      
      response = client.delete(reverse('update_endpoints', kwargs={'pk': pk}), content_type='application/json')
      
      self.assertEqual(response.status_code, not_found)
      
      print('\n Invalid deletion checked successfuly')
      
   
      
      
      
      
      