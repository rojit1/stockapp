from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from stock_market.models import Company,CompanyData
from .serializers import CompanyDataSerializer

class DailyData(APIView):

    permission_classes = AllowAny,

    def get(self,request, symbol):
        company = get_object_or_404(Company,stock_symbol=symbol)
        company_data = CompanyData.objects.filter(company=company)
        serializer = CompanyDataSerializer(instance=company_data, many=True)
        return Response({'data':serializer.data,'count':len(company_data)}, status=status.HTTP_200_OK)