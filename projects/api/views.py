from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from projects.models import Project
from .serializers import ProjectSerializer, ProjectCreateSerializer, ProjectUpdateSerializer
from .permissions import CanAccessProject, CanCreateProject, CanEditProject

class ProjectListCreateView(generics.ListCreateAPIView):
    
    permission_classes = [IsAuthenticated, CanCreateProject]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_super_admin:
            return Project.objects.all().select_related('country', 'created_by', 'updated_by')
        elif user.is_country_admin or user.is_member:
            return Project.objects.filter(country=user.country).select_related('country', 'created_by', 'updated_by')
        
        return Project.objects.none()
    
    def perform_create(self, serializer):
        project = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )
        project._audit_user = self.request.user  
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        project = Project.objects.get(id=serializer.instance.id)
        read_serializer = ProjectSerializer(project, context={'request': request})
        
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
class ProjectDetailView(generics.RetrieveAPIView):
   
    queryset = Project.objects.all().select_related('country', 'created_by', 'updated_by')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, CanAccessProject]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_super_admin:
            return Project.objects.all().select_related('country', 'created_by', 'updated_by')
        elif user.is_country_admin or user.is_member:
            return Project.objects.filter(country=user.country).select_related('country', 'created_by', 'updated_by')
        
        return Project.objects.none()
    
class ProjectUpdateView(generics.UpdateAPIView):
    
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, CanEditProject]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectUpdateSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_super_admin:
            return Project.objects.all().select_related('country', 'created_by', 'updated_by')
        elif user.is_country_admin:
            return Project.objects.filter(country=user.country).select_related('country', 'created_by', 'updated_by')
        
        return Project.objects.none()
    
    def perform_update(self, serializer):
        project = serializer.save(updated_by=self.request.user)
        project._audit_user = self.request.user 
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        project = Project.objects.get(id=instance.id)
        read_serializer = ProjectSerializer(project, context={'request': request})
        
        return Response(read_serializer.data)

class ProjectDeleteView(generics.DestroyAPIView):
   
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, CanEditProject]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_super_admin:
            return Project.objects.all()
        elif user.is_country_admin:
            return Project.objects.filter(country=user.country)
        
        return Project.objects.none()
    
    def perform_destroy(self, instance):
        instance._audit_user = self.request.user 
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        project_title = instance.title
        self.perform_destroy(instance)
        
        return Response(
            {'detail': f'Project "{project_title}" has been deleted successfully.'},
            status=status.HTTP_200_OK
        )