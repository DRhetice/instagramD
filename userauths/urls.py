from django.urls import path
from userauths import views

urlpatterns = [
    path('<username>/', views.userProfile, name='profile'),
    path('<username>/saved/', views.userProfile, name='profilefavorite'),
    path('<username>/follow/<option>', views.follow, name='follow'),
    path('<username>/editprofile', views.editProfile, name='edit-profile'),
    ]
