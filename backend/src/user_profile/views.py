from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
Account = get_user_model()

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializer


class ProfileDetailView(APIView):

    def get(self, request):
        user = get_object_or_404(Account, pk=request.user.id)
        serializer = ProfileSerializer(instance=user)
        return Response(serializer.data)
