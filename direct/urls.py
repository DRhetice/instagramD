from django.urls import path
from direct import views

urlpatterns = [
    path('inbox/', views.inbox, name='message'),
     path('direct/<username>', views.Directs, name="directs"),
    path('send/', views.SendDirect, name="send-directs"),
    path('search/', views.UserSearch, name="search-users"),
    path('new/<username>', views.NewConversation, name="conversation"),
]
