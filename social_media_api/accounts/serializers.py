from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    bio = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'bio', 'birth_date', 'profile_picture', 'followers']
        read_only_fields = ['id', 'followers']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data.get('password'),
            bio=validated_data.get('bio', ''),
            birth_date=validated_data.get('birth_date', None),
            profile_picture=validated_data.get('profile_picture', None)
        )
        Token.objects.create(user=user)
        return user
    
    def validate(self, data):
       # validate credentials
       data['user'] = get_user_model().objects.get(username=data['username'])
       return data
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'birth_date', 'profile_picture', 'followers']
        read_only_fields = ['id', 'username', 'email', 'followers']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            try:
                user = get_user_model().objects.get(username=username)
            except get_user_model().DoesNotExist:
                raise serializers.ValidationError("Invalid username or password.")
            
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Both username and password are required.")
        
        data['user'] = user
        return data
    
