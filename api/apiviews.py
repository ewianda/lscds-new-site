from rest_framework import routers, serializers, viewsets
from registration.users import UserModel, UserModelString
from django.db.models import Q,Count
User=UserModel()
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'last_name', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()[1:5]
    serializer_class = UserSerializer
