from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/<str:email>/<str:password>/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('getfeedbacks/<str:email>/', views.getfeedbacks, name='getfeedbacks'),
    path('feedbacks/<str:email>/<str:title>/<str:category>/<str:message>/<str:anonymous>/', views.feedbacks, name='feedbacks'),
]