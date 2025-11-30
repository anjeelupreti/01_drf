from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from audits.models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
   
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
       
        user = self.request.user
        
        queryset = AuditLog.objects.all().select_related('user')
        
        if user.is_super_admin:
            return queryset
        elif user.is_country_admin:
            
            return queryset.filter(
                Q(user__country=user.country) | 
                Q(user=user)  
            )
        else:
            return queryset.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        
        logs = AuditLog.objects.filter(user=request.user).select_related('user')
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_model(self, request):
        
        model_name = request.query_params.get('model', None)
        queryset = self.get_queryset()
        
        if model_name:
            queryset = queryset.filter(model_name=model_name)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get']) 
    def by_action(self, request):
      
        action_type = request.query_params.get('action', None)
        queryset = self.get_queryset()
        
        if action_type:
            queryset = queryset.filter(action=action_type)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)