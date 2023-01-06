from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('room/<str:pk>',views.room,name='room'),
    path('create_rooms/',views.create_rooms,name='create_room'),
    path('update_room/<str:pk>',views.update_room,name='update_room'),
    path('delete_room/<str:pk>',views.delete_room,name='delete_room'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('register/',views.register,name='register'),
    path('delete_message/<str:pk>',views.delete_message,name='delete_message'),
    path('profile/<str:pk>',views.profile,name='profile')
]