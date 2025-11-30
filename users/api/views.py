from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from users.models import User, Country
from .serializers import (
    UserSerializer, UserCreateSerializer, UserLoginSerializer, 
    CountrySerializer
)
from .permissions import IsSuperAdmin, IsCountryAdminOrSuperAdmin

class BaseUserView:
    permission_classes = [IsAuthenticated, IsCountryAdminOrSuperAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin:
            return User.objects.all().select_related('country')
        elif user.is_country_admin:
            return User.objects.filter(country=user.country).select_related('country')
        return User.objects.none()

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
 
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            
            user_data = UserSerializer(user).data
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials or inactive account'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(BaseUserView, generics.ListAPIView):
    serializer_class = UserSerializer

class UserCreateView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, IsCountryAdminOrSuperAdmin]
    
    def perform_create(self, serializer):
        
        user = serializer.save()
        user._audit_user = self.request.user  

class UserDetailView(BaseUserView, generics.RetrieveAPIView):
    serializer_class = UserSerializer

class UserUpdateView(BaseUserView, generics.UpdateAPIView):
   
    serializer_class = UserSerializer
    
    def perform_update(self, serializer):
        
        user = serializer.save()
        user._audit_user = self.request.user 

class UserDeleteView(BaseUserView, generics.DestroyAPIView):
   
    def perform_destroy(self, instance):
       
        instance._audit_user = self.request.user  
        instance.delete()

class CountryListView(generics.ListAPIView):
    """
    List all countries
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_super_admin:
            return Country.objects.all()
        elif user.is_country_admin:
            return Country.objects.filter(id=user.country_id)
        
        return Country.objects.all()