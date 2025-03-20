
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('complain_compliment_app.urls')),
    path('admin/', admin.site.urls),
]
