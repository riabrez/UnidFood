from django.urls import path
from unidfood import views

app_name = 'unidfood'
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_review/', views.add_review, name='add_review'),
    path('my_reviews/', views.my_reviews, name='my_reviews'),
    path('my_meetups/', views.my_meetups, name='my_meetups'),
    path('deals/', views.deals, name='deals'),
    path('places/', views.places, name='places'),
    path('place/<int:place_id>/', views.place_detail, name='place_detail'),
    path('nearby/', views.nearby, name='nearby'),
    path('search/', views.search, name='search'),
]