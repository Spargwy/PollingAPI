from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from polling.api.viewsets import PollViewSet, LoginView

router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls')

schema_view = get_schema_view(
    openapi.Info(
        title="Test API",
        default_version='v1',
        description="Test description"
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = router.get_urls() + [
    path('login/', LoginView.as_view(), name='login'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
