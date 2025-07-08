from django.urls import path
from . import views

app_name = 'photos'

urlpatterns = [
    path('create_photo/', views.create_photo, name='create_photo'),
    path('photo_details/<int:pk>/', views.photo_details, name='photo_details'),
    path('edit_photo/<int:pk>/', views.edit_photo, name='edit_photo'),
    path('delete_photo/<int:pk>/', views.delete_photo, name='delete_photo'),
    path('like/<int:pk>/', views.like_toggle, name='like_toggle'),
    path('photo/<int:pk>/share/', views.share_photo, name='share_photo'),
]