from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointment_history, name='appointment_history'),
    path('appointments/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
]
