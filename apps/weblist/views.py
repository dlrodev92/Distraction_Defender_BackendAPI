from rest_framework import viewsets
from .models import WebList
from .serializers import WebListSerializer

# Create your views here.WebListSerializer
class WebListViewSet(viewsets.ModelViewSet):
    queryset = WebList.objects.all()
    serializer_class = WebListSerializer