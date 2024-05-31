from django.urls import path, include
from . import views


urlpatterns = [
    path('register/job_seeker/', views.EmployerRegisterAPIView.as_view(), name='job-seeker-register'),
    path('register/employer/', views.EmployerRegisterAPIView.as_view(), name='employer-register'),
    path('verify-employer/', views.VerifyEmployerPhoneNumber.as_view(), name='verify-employer'),
    path('login/job_seeker/', views.JobSeekerLoginAPIView.as_view(), name='job-seeker-login'),
    path('login/employer/', views.EmployerLoginAPIView.as_view(), name='employer-login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('forgot-password/', views.ForgotPasswordRequestAPIView.as_view(), name='forgot-password'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmAPIView.as_view(), name='reset-password-confirm'),
    path('set-new-password/', views.SetNewPasswordAPIView.as_view(), name='set-new-password'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name='change-password'),
]