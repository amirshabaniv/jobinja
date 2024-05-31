from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.api.urls')),
    path('', include('companies.api.urls')),
    path('', include('ads.api.urls')),
]
