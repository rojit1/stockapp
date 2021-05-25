from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


from rest_framework import  serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import Account

# serializer for registering user
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = 'email', 'firstname', 'lastname', 'password', 'country'
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

# serilizer for Login
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

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6,max_length=30)
    uid = serializers.CharField(max_length=100)
    token = serializers.CharField(max_length=100)

    def validate(self, attrs):
        password = attrs.get('password', '')
        uid = attrs.get('uid', '')
        token = attrs.get('token', '')
        try:
            id = int(force_str(urlsafe_base64_decode(uid)))
            user = Account.objects.get(pk=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The link is invalid', 401)
            user.set_password(password)
            user.save()
        except Exception:
            raise AuthenticationFailed('The link is invalid', 401)
        return attrs



