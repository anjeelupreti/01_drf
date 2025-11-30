from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from projects.models import Project
from users.api.serializers import CountrySerializer, UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
   
    country_details = CountrySerializer(source='country', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    updated_by_details = UserSerializer(source='updated_by', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'status', 'status_display',
            'country', 'country_details', 
            'created_by', 'created_by_details',
            'updated_by', 'updated_by_details',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_by', 'updated_by', 
            'created_at', 'updated_at', 'status_display'
        ]
        extra_kwargs = {
            'country': {'write_only': True}
        }

class ProjectCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'country']
    
    def validate(self, attrs):
        
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            country = attrs.get('country')
            
            if user.is_super_admin:
                return attrs
            
            if (user.is_country_admin or user.is_member) and user.country != country:
                raise serializers.ValidationError({
                    'country': 'You can only create projects for your assigned country.'
                })
        
        return attrs

class ProjectUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'country']
    
    def validate(self, attrs):
        
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            country = attrs.get('country')
            
            if user.is_super_admin:
                return attrs
            
            if user.is_country_admin and user.country != country:
                raise serializers.ValidationError({
                    'country': 'You can only update projects for your assigned country.'
                })
            
            if user.is_member:
                raise serializers.ValidationError({
                    'detail': 'Members do not have permission to update projects.'
                })
        
        return attrs
    
    def update(self, instance, validated_data):
    
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance