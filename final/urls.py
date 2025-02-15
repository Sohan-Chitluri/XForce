from django.contrib import admin
from django.urls import path, include
from prof import views  # Import the profile view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('prof.urls')),  # This will include additional URLs from prof.urls
]
