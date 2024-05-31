from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('home', views.ListAdsViewSet, basename='list-ads')
router.register('save', views.SaveViewSet, basename='saved'),

urlpatterns = [
    path('', include(router.urls)),

    # Employer
    path('create/ad/', views.CreateAdAPIView.as_view(), name='create-ad'),
    path('delete/ad/<int:pk>/', views.DeleteAdAPIView.as_view(), name='create-ad'),
    path('my-ads/<int:ad_id>/resumes', views.EmployerGetResumesAPIView.as_view(), name='get-resumes'),
    path('my-ads/<int:ad_id>/resumes/<int:resume_id>/', views.EmployerGetResumeAPIView.as_view(), name='get-resume'),
    path('my-ads/<int:ad_id>/resumes/<int:resume_id>/interview', views.InterviewJobSeekerAPIView.as_view(), name='interview-job-seeker'),
    path('my-ads/<int:ad_id>/resumes/<int:resume_id>/response', views.ResponseAPIView.as_view(), name='response'),
    path('my-ads/', views.EmployerAdsAPIView.as_view(), name='my-ads'),
    path('my-ads/<int:ad_id>/', views.EmployerAdAPIView.as_view(), name='my-ad'),
    
    # Employer and job seeker
    path('ads/<int:pk>/', views.RetrieveAdAPIView.as_view(), name='retrieve-ad'),
    path('my-saves/', views.MySaveAPIView.as_view(), name='my-saves'),
    
    # Job seeker
    path('jobs/applied/', views.JobSeekerAppliesAPIView.as_view(), name='my-applies'),
    path('jobs/applied/<int:resume_id>/details/', views.JobSeekerResumeDetailAPIView.as_view(), name='apply-detail')
]