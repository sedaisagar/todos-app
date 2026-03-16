from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Added Later
    path('', include('todos.urls')),
]
