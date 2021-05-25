from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from decouple import config

from .serializers import RegisterSerializer, LoginSerializer, SetNewPasswordSerializer
from .utils import Util
from django.contrib.auth import get_user_model
Account = get_user_model()


class RegisterView(APIView):
    permission_classes = AllowAny,

    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #save user and get for sending email
        user = Account.objects.get(email=serializer.data['email'])

        current_site = get_current_site(request).domain
        relative_link = reverse('account:verify-email')
        token = str(RefreshToken.for_user(user).access_token)
        absurl = config('SSL')+'://'+current_site+relative_link+'?token='+token
        email_body = "Hello, please use the link to activate your account \n"+absurl
        data = {'body':email_body, 'to':user.email, 'subject':'Verify your email'}
        Util.send_email(data)
        return Response({'details':'Please check your email and verify your account','data':serializer.data}, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):

    permission_classes = AllowAny,

    # function to get token and verify user
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY, algorithms='HS256')
            user = Account.objects.get(id = payload['user_id'])
            user.is_active = True
            user.save()
            return Response({'details':'Account successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    permission_classes = AllowAny,

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response =  Response()
        response.set_cookie(key='access',value=serializer.data['tokens']['access'], httponly=True)
        del serializer.data['tokens']['access']
        response.data = {
            'data':serializer.data
        }
        return response


class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(APIView):

    permission_classes = AllowAny,

    def post(self, request):
        email = request.data.get('email','')

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            if not user.is_active:
                return Response({'details':'The provided account doesnot exists'}, status=status.HTTP_404_NOT_FOUND)

            uid = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('account:token-check', kwargs={'uid':uid,'token':token})
            abs_url = config('SSL')+'://'+current_site+relative_link
            body = "Hello, use the link below to reset your password \n"+abs_url
            data = {'subject':'Reset your password','body':body, 'to':user.email}
            Util.send_email(data)
            return Response({'details':'The password reset link is sent in mail'}, status=status.HTTP_200_OK)

        return Response({'details':'The provided email doesnot exists'}, status=status.HTTP_404_NOT_FOUND)


class PasswordTokenCheckView(APIView):

    permission_classes = AllowAny,

    def get(self, request, uid, token):
        try:
            id = force_str(smart_bytes(urlsafe_base64_decode(uid)))
            user = Account.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'details':'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'details':'Success','data':{'uid':uid,'token':token}}, status=status.HTTP_200_OK)


        except DjangoUnicodeDecodeError:
            return Response({'details':'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        except Account.DoesNotExist:
            return Response({'details':"The user account doesnot exists"}, status=status.HTTP_404_NOT_FOUND)


class SetNewPasswordView(APIView):
    permission_classes = AllowAny,
    def patch(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'details':'Password reset successful'}, status=status.HTTP_200_OK)

