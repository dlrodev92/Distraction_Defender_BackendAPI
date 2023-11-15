from rest_framework.routers import DefaultRouter
from .views import WebListViewSet

router = DefaultRouter()
router.register(r'weblist', WebListViewSet, basename='weblist')
urlpatterns = router.urls