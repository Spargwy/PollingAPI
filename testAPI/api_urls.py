from rest_framework.routers import DefaultRouter

from polling.api.viewsets import PollViewSet

router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls')
urlpatterns = router.get_urls()
