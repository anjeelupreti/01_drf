from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='auth-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    # Country endpoints
    path('countries/', views.CountryListView.as_view(), name='country-list'),
]
