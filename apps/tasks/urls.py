from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls