from django.urls import path
from . import api_views

urlpatterns = [
   path('puppies/',api_views.puppies_api, name='get_and_post'),
   path('puppies/<int:pk>/',api_views.puppies_api2, name='update_endpoints'),

]