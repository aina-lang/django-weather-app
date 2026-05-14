from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Auth
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.register, name='register'),
    
    path('api/weather/', views.weather_search, name='weather_search'),
    path('api/cluster-info/', views.cluster_info, name='cluster-info'),
    path('api/health/', views.health_check, name='health_check'),
]
