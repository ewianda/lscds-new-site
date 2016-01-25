from rest_framework import routers, serializers, viewsets
from registration.users import UserModel, UserModelString
from django.db.models import Q,Count
from rest_framework import generics
from event.models import *
User=UserModel()
from rest_framework.views import APIView
# Serializers define the API representation.
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        



class UserSerializer(serializers.HyperlinkedModelSerializer):
 
    registered_list = serializers.SerializerMethodField()
    not_registered_list = serializers.SerializerMethodField()
    event_history= serializers.SerializerMethodField()
    
    
    def get_registered_list(self, obj):
         serializer =  EventSerializer(Event.objects.user_events(obj), many=True)
         return serializer.data
    def get_not_registered_list(self, obj):
         serializer = EventSerializer(Event.objects.user_open_events(obj), many=True)
         return serializer.data
    def get_event_history(self, obj):
        serializer = EventSerializer(Event.objects.user_event_history(obj), many=True)
        return serializer.data
    
    class Meta:
        model = User
        fields = ('url', 'last_name', 'email', 'event_history','not_registered_list','registered_list')
        
 
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.filter(id__lte=10)
    serializer_class = UserSerializer

    
    
    
    
class UserProfileApi(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    