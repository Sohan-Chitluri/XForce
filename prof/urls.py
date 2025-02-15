from django.urls import path
from . import views  # Import views.py

urlpatterns = [
    path('', views.home, name="home"),  
    path('profile/', views.profile, name="profile"),  
    path('upload/', views.update_profile, name='update_profile'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("schedule/", views.schedule_list, name="schedule_list"), 
    path('add/', views.add_schedule, name='add_schedule'),
   # path('list/', views.schedule_list, name='schedule_list'),  
    path('delete/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),  
]

