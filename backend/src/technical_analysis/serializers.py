from rest_framework import fields, serializers
from stock_market.models import CompanyData


class CompanyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyData
        fields = '__all__'