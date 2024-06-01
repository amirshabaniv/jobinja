from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from companies.models import Company
from .serializers import CompanySerializer, CreateCompanySerializer
from permissions import IsEmployer
from paginations import CustomPagination
from ads.models import Ad
from ads.api.serializers import AdForListSerializer


class CreateCompanyAPIView(CreateAPIView):
    serializer_class = CreateCompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)


class ListCompaniesAPIView(ListAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    pagination_class = CustomPagination


class RetrieveCompanyAPIView(GenericAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def get(self, request, name_en):
        try:
            company = Company.objects.get(name_en=name_en)
            serializer = self.serializer_class(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'error':'Company not found'}, status=status.HTTP_400_BAD_REQUEST)


class FieldOfActivityAPIView(GenericAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    pagination_class = CustomPagination
    
    def get(self, request, field_name):
        companies = Company.objects.filter(field_of_activity__name_en=field_name)
        if companies.exists():
            page = self.paginate_queryset(companies)  
            if page is not None:
                srz = self.serializer_class(page, many=True)
                return self.get_paginated_response(srz.data)  
            serializer = self.serializer_class(companies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'Companies not found'}, status=status.HTTP_400_BAD_REQUEST)


class CompanyAdsAPIView(GenericAPIView):
    serializer_class = AdForListSerializer
    queryset = Ad.objects.all()
    pagination_class = CustomPagination

    def get(self, request, name_en):
        ads = Ad.objects.filter(company__name_en=name_en)
        if ads.exists():
            page = self.paginate_queryset(ads)  
            if page is not None:
                srz = self.serializer_class(page, many=True)
                return self.get_paginated_response(srz.data)  
            serializer = self.serializer_class(ads, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'Ads not found'}, status=status.HTTP_400_BAD_REQUEST)








