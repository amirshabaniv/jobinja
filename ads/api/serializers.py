from rest_framework import serializers
from ads.models import Ad, Resume, Save
from companies.api.serializers import CompanySerializer


class AdForListSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    company_logo = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'title', 'type_of_cooperation',
                  'salary', 'province', 'city', 'company_name',
                  'company_logo', 'created_at']
        
    def get_company_name(self, ad):
        return ad.company.name_en
    
    def get_company_logo(self, ad):
        return ad.company.logo.url
    

class CreateAdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = ['id', 'title', 'category', 'type_of_cooperation',
                  'work_experience', 'salary', 'description',
                  'skill', 'province', 'city', 'created_at']
        

class AdForRetrieveSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Ad
        fields = ['id', 'title', 'category', 'type_of_cooperation',
                  'work_experience', 'salary', 'description',
                  'skill', 'employer', 'company', 'province', 'city', 'created_at']


class ResumeForEmployerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resume
        fields = ['id', 'file', 'job_seeker', 'ad']


class ResumeForJobSeekerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resume
        fields = ['id', 'file', 'job_seeker', 'ad', 'phone_number']


class ResumeForJobSeekerAppliesSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    ad_title = serializers.SerializerMethodField()
    company_logo = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'title', 'company_name', 'status', 'created_at']
    
    def get_company_name(self, resume):
        return resume.ad.company.name_en
    
    def get_ad_title(self, resume):
        return resume.ad.title
    
    def get_company_logo(self, resume):
        return resume.ad.company.logo.url
    

class CreateDestroySaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Save
        fields = ['id', 'ad']


class SaveSerializer(serializers.ModelSerializer):
    ad = AdForListSerializer()

    class Meta:
        model = Save
        fields = ['id', 'ad']