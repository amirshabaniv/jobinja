from rest_framework import serializers
from companies.models import Company, City, Province, FieldOfActivity


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name_fa', 'name_en', 'logo', 'image',
                  'phone_number', 'website', 'field_of_activity',
                  'number_of_staff', 'description', 'province',
                  'city', 'employer', 'established']
        

class CreateCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name_fa', 'name_en', 'logo', 'image',
                  'phone_number', 'website', 'field_of_activity',
                  'number_of_staff', 'description', 'province',
                  'city', 'established']
    
    