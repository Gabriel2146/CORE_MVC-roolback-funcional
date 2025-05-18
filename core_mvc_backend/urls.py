from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({"message": "Welcome to the Core MVC Training API"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/training/', include('training.urls')),
    path('api/wger/', include('wger_integration.urls')),
    path('', api_root),
]
