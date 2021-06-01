from django.urls import path
from rest_framework.routers import DefaultRouter

from polling.api.viewsets import PollViewSet, LoginView

router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls')

urlpatterns = router.get_urls() + [
    path('login/', LoginView.as_view(), name='login'),
]
