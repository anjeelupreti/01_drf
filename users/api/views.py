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
    """
    User login endpoint that returns JWT tokens
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Authenticate user
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_active:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Get user data
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
    """
    Create new users with role-based permissions
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, IsCountryAdminOrSuperAdmin]

class UserDetailView(BaseUserView, generics.RetrieveAPIView):
    serializer_class = UserSerializer

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
            # Super Admin can see all countries
            return Country.objects.all()
        elif user.is_country_admin:
            # Country Admin can only see their own country
            return Country.objects.filter(id=user.country_id)
        
        # Members can see all countries (or adjust as needed)
        return Country.objects.all()