from rest_framework import serializers
from apps.weblist.models import WebList

class WebListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebList
        fields = ('id', 'user', 'title', 'urls_json')
        extra_kwargs = {'user': {'read_only': True}}
        
   