from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    # Django admin
    path('admin/', admin.site.urls),

    # User management
    path('accounts/', include('django.contrib.auth.urls')),

    # Local apps
    path('api/', include('api.urls')),
    path('users/', include('users.urls')),
]
