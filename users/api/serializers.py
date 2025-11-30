from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import User, Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']

class UserSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source='country', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 
            'role', 'country', 'country_details', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'country': {'write_only': True}
        }

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'password', 
            'password_confirm', 'role', 'country'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords don't match."})
        
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            creating_user = request.user
            target_role = attrs.get('role')
            target_country = attrs.get('country')
            
            if not creating_user.can_create_users_for_country(target_country):
                raise serializers.ValidationError(
                    "You don't have permission to create users for this country."
                )
            
            if (creating_user.is_country_admin and 
                target_role != User.Role.MEMBER):
                raise serializers.ValidationError(
                    "Country Admin can only create Member users."
                )
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            **validated_data,
            password=password
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()