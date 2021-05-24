from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework import  serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import Account

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = 'email', 'firstname', 'lastname', 'password', 'country'
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    tokens = serializers.SerializerMethodField()
    access_token_lifetime = serializers.IntegerField(read_only=True)

    def get_tokens(self, obj):
        user = Account.objects.get(email=obj['email'])
        return {
            'refresh':user.tokens()['refresh'],
            'access':user.tokens()['access']
        }

    class Meta:
        model = Account
        fields = 'email', 'password', 'tokens', 'access_token_lifetime'
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')

        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_active:
            raise AuthenticationFailed('Users account is not activated')
        return {
            'email':user.email,
            'access_token_lifetime':settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds
        }