from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api_users.views import UserViewSet, send_confirmation_code, send_token

router = DefaultRouter()
router.register('users', UserViewSet, basename='User')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('api.urls')),
    path('auth/email/', send_confirmation_code, name='email_confirm'),
    path('auth/token/', send_token, name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
