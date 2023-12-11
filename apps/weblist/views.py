from rest_framework import viewsets
from .models import WebList
from .serializers import WebListSerializer

# Create your views here.WebListSerializer
class WebListViewSet(viewsets.ModelViewSet):
    queryset = WebList.objects.all()
    serializer_class = WebListSerializer
    
    def get_queryset(self):
        # Filter the queryset based on the current authenticated user
        return WebList.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Set the user field to the current authenticated user as we have the global authentication on the settings file, the reques will be checked for authentication
        # and the user will be set to the current authenticated user
        serializer.save(user=self.request.user)
        
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)