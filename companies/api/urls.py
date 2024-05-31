from django.urls import path, include

from . import views

urlpatterns = [
    path('companies/', views.ListCompaniesAPIView.as_view(), name='list-companies'),
    path('companies/<str:name_en>/', views.RetrieveCompanyAPIView.as_view(), name='retrieve-companies'),
    path('create/company/', views.CreateCompanyAPIView.as_view(), name='create-company'),
    path('companies/<str:field_name>/', views.FieldOfActivityAPIView.as_view(), name='field-of-activity'),
    path('companies/<str:name_en>/jobs/', views.CompanyAdsAPIView.as_view(), name='companie-ads'),
]