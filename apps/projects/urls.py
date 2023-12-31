from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls