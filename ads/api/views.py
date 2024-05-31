from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ads.models import Ad, Resume, Save
from .serializers import (AdForListSerializer,
                          CreateAdSerializer,
                          AdForRetrieveSerializer,
                          ResumeForEmployerSerializer,
                          ResumeForJobSeekerSerializer,
                          ResumeForJobSeekerAppliesSerializer,
                          CreateDestroySaveSerializer,
                          SaveSerializer)
from permissions import IsEmployer, IsOwner, IsOwner2
from .filters import AdFilter
from paginations import CustomPagination


class ListAdsViewSet(ListModelMixin, GenericViewSet):
    serializer_class = AdForListSerializer
    queryset = Ad.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AdFilter
    search_fields = ['title', 'company__name_en', 'company__name_fa', 'skill__name']
    ordering_fields = ['created_at']
    pagination_class = CustomPagination


class CreateAdAPIView(CreateAPIView):
    serializer_class = CreateAdSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user, company=self.request.user.company)


class DeleteAdAPIView(DestroyAPIView):
    serializer_class = AdForRetrieveSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated, IsEmployer, IsOwner]


class RetrieveAdAPIView(GenericAPIView):
    serializer_class = AdForRetrieveSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            ad = Ad.objects.get(pk=pk)
            serializer = self.serializer_class(ad)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ad.DoesNotExist:
            return Response({'error':'Ad not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, pk):
        try:
            ad = Ad.objects.get(pk=pk)
            file = request.data.get('file')
            if request.user.is_job_seeker:
                resume = Resume.objects.create(
                    file=file,
                    job_seeker=request.user,
                    ad=ad
                )
                resume.send_resume()
                return Response({'message':'Resume sent successfully'}, status=status.HTTP_201_CREATED)
            return Response({'error':'You are not job seeker'}, status=status.HTTP_400_BAD_REQUEST)
        except Ad.DoesNotExist:
            return Response({'error':'Ad not found'}, status=status.HTTP_400_BAD_REQUEST)


class EmployerGetResumesAPIView(GenericAPIView):
    serializer_class = ResumeForEmployerSerializer
    queryset = Resume.objects.all()

    def get(self, request, ad_id):
        try:
            ad = Ad.objects.get(pk=ad_id)
            if (request.user.is_employer) and (ad.employer == request.user):
                resumes = Resume.objects.filter(ad=ad)
                serializer = self.serializer_class(resumes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error':'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
        except Ad.DoesNotExist:
            return Response({'error':'Ad not found'}, status=status.HTTP_400_BAD_REQUEST)
    

class EmployerGetResumeAPIView(GenericAPIView):
    serializer_class = ResumeForEmployerSerializer
    queryset = Resume.objects.all()

    def get(self, request, ad_id, resume_id):
        try:
            ad = Ad.objects.get(pk=ad_id)
            if (request.user.is_employer) and (ad.employer == request.user):
                resume = Resume.objects.get(ad=ad, pk=resume_id)
                resume.review_resume()
                serializer = self.serializer_class(resume)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error':'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
        except Ad.DoesNotExist:
            return Response({'error':'Ad not found'}, status=status.HTTP_400_BAD_REQUEST)


class InterviewJobSeekerAPIView(GenericAPIView):
    serializer_class = ResumeForEmployerSerializer
    queryset = Resume.objects.all()

    def get(self, request, ad_id, resume_id):
        try:
            ad = Ad.objects.get(pk=ad_id)
            if (request.user.is_employer) and (ad.employer == request.user):
                resume = Resume.objects.get(ad=ad, pk=resume_id)
                resume.interview()
                return Response({'message':'resume status changed to interview successfully'}, status=status.HTTP_200_OK)
            return Response({'error':'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
        except Ad.DoesNotExist:
            return Response({'error':'Ad not found'}, status=status.HTTP_400_BAD_REQUEST)


class ResponseAPIView(GenericAPIView):
    serializer_class = ResumeForEmployerSerializer
    queryset = Resume.objects.all()

    def post(self, request, ad_id, resume_id):
        try:
            response = request.data.get('response')
            ad = Ad.objects.get(pk=ad_id)
            if (request.user.is_employer) and (ad.employer == request.user):
                resume = Resume.objects.get(ad=ad, pk=resume_id)
                resume.response(response)
                return Response({'message':'response sent successfully'}, status=status.HTTP_200_OK)
            return Response({'error':'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
        except Ad.DoesNotExist:
            return Response({'error':'Ad not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class EmployerAdsAPIView(GenericAPIView):
    serializer_class = AdForListSerializer
    queryset = Ad.objects.all()

    def get(self, request):
        try:
            if (request.user.is_employer):
                ads = Ad.objects.filter(employer=request.user)
                serializer = self.serializer_class(ads)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error':'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
        except Ad.DoesNotExist:
            return Response({'error':'Ads not found'}, status=status.HTTP_400_BAD_REQUEST)

        
class EmployerAdAPIView(GenericAPIView):
    serializer_class = AdForRetrieveSerializer
    queryset = Ad.objects.all()

    def get(self, request, ad_id):
        try:
            if (request.user.is_employer):
                ad = Ad.objects.get(employer=request.user, pk=ad_id)
                serializer = self.serializer_class(ad)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error':'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
        except Ad.DoesNotExist:
            return Response({'error':'Ad not found'}, status=status.HTTP_400_BAD_REQUEST)


class JobSeekerAppliesAPIView(GenericAPIView):
    serializer_class = ResumeForJobSeekerAppliesSerializer
    queryset = Resume.objects.all()

    def get(self, request):
        try:
            if (request.user.is_job_seeker):
                resumes = Resume.objects.filter(job_seeker=request.user)
                serializer = self.serializer_class(resumes)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error':'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
        except Resume.DoesNotExist:
            return Response({'error':'Resumes not found'}, status=status.HTTP_400_BAD_REQUEST)


class JobSeekerResumeDetailAPIView(GenericAPIView):
    serializer_class = ResumeForJobSeekerSerializer
    queryset = Resume.objects.all()

    def get(self, request, resume_id):
        try:
            if (request.user.is_job_seeker):
                resume = Resume.objects.get(job_seeker=request.user, pk=resume_id)
                serializer = self.serializer_class(resume)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error':'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
        except Resume.DoesNotExist:
            return Response({'error':'Resume not found'}, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, resume_id):
        try:
            if (request.user.is_job_seeker):
                new_file = request.FILES.get('file')
                resume = Resume.objects.get(job_seeker=request.user, pk=resume_id)
                resume.file = new_file
                resume.save()
                return Response({'message':'resume updated successfully'}, status=status.HTTP_200_OK)
        except Resume.DoesNotExist:
            return Response({'error':'Resume not found'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, resume_id):
        try:
            if (request.user.is_job_seeker):
                resume = Resume.objects.get(job_seeker=request.user, pk=resume_id)
                resume.delete()
                return Response({'message':'resume deleted successfully'}, status=status.HTTP_200_OK)
        except Resume.DoesNotExist:
            return Response({'error':'Resume not found'}, status=status.HTTP_400_BAD_REQUEST)

            
class SaveViewSet(CreateModelMixin, DestroyModelMixin,  GenericViewSet):
    serializer_class = CreateDestroySaveSerializer
    queryset = Save.objects.all()
    permission_classes = [IsAuthenticated, IsOwner2]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MySaveAPIView(GenericAPIView):
    serializer_class = SaveSerializer
    queryset = Save.objects.all()
    pagination_class = CustomPagination

    def get(self, request):
        saves = Save.objects.filter(user=request.user)
        if saves.exists():
            page = self.paginate_queryset(saves)  
            if page is not None:
                srz = self.serializer_class(page, many=True)
                return self.get_paginated_response(srz.data)  
            serializer = self.serializer_class(saves, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'saves not found'}, status=status.HTTP_400_BAD_REQUEST)
            








