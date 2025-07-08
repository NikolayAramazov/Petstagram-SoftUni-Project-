from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.root_redirect, name='root_redirect'),
    path('home/', views.home, name='home'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('register/', views.register, name='register'),
    path('sign_out/', views.sign_out, name='sign_out'),

    # Profile URLs
    path('profile/<int:pk>/', views.profile_details, name='profile_details'),
    path('profile/<int:pk>/edit/', views.edit_profile, name='profile_edit'),
    path('profile/<int:pk>/delete/', views.profile_delete, name='profile_delete'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('chat/<str:username>/', views.chat, name='chat'),
]
