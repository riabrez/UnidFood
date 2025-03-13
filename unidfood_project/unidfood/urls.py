from django.urls import path
from unidfood import views

app_name = 'unidfood'

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]