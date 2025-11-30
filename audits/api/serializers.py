from rest_framework import serializers
from audits.models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    # Add user details to make the response more readable
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id',
            'action',
            'user',         
            'user_email',     
            'user_role',      
            'model_name', 
            'object_id',
            'object_repr',
            'changes',
            'timestamp'
        ]
        read_only_fields = fields  