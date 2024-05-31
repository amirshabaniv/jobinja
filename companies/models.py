from django.db import models
from accounts.models import Employer
from django.contrib.auth import get_user_model
User = get_user_model()


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    provine = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class FieldOfActivity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Company(models.Model):
    NUMBER_OF_STAFF = (
        ('2-10 نفر', '2-10 نفر'),
        ('11-50 نفر', '11-50 نفر'),
        ('51-200 نفر', '51-200 نفر'),
        ('201-500 نفر', '201-500 نفر'),
        ('501-1000 نفر', '501-1000 نفر'),
        ('بیش از 1000 نفر', 'بیش از 1000 نفر')
    )

    name_fa = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='media/logo_images/', null=True, blank=True)
    image = models.ImageField(upload_to='media/company_images/', null=True, blank=True)
    phone_number = models.CharField(max_length=11)
    website = models.URLField(null=True, blank=True)
    field_of_activity = models.ManyToManyField(FieldOfActivity, related_name='companies')
    number_of_staff = models.CharField(max_length=80, choices=NUMBER_OF_STAFF)
    description = models.TextField()
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='companies')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='companies')
    employer = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='company')
    established = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name_fa




