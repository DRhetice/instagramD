from django.urls import path
from userauths import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #User Auth
    path('sign-up/',views.register, name="sign-up"),
    path('sign-in/', auth_views.LoginView.as_view(template_name="sign-in.html", redirect_authenticated_user=True), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(template_name="sign-out.html"), name='sign-out'), 

    path('<username>/', views.userProfile, name='profile'),
    path('<username>/saved/', views.userProfile, name='profilefavorite'),
    path('<username>/follow/<option>', views.follow, name='follow'),
    path('<username>/editprofile', views.editProfile, name='edit-profile'),
    ]
