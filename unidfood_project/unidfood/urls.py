from django.urls import path
from unidfood import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
app_name = 'unidfood'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
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
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('change_password/', views.change_password, name='change_password'),
    path('goodbye/', views.goodbye, name='goodbye'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html',
        email_template_name='account/password_reset_email.html',
        success_url=reverse_lazy('unidfood:password_reset_done') 
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html',
        success_url=reverse_lazy('unidfood:password_reset_complete')
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'
    ), name='password_reset_complete'),

]