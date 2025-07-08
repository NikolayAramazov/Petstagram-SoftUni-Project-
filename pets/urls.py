from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('add_pet',views.add_pet,name='add_pet'),
    path('pet_details/<int:pk>',views.pet_details,name='pet_details'),
    path('pet_edit/<int:pk>',views.pet_edit,name='pet_edit'),
    path('pet_delete/<int:pk>',views.pet_delete,name='pet_delete'),
]
