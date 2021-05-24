from django.contrib.auth import get_user_model
Account = get_user_model()

from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = 'email', 'firstname', 'lastname', 'country', 'phone'