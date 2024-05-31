from ads.models import Ad, Province
from companies.models import FieldOfActivity

from django_filters import rest_framework as filters


class AdFilter(filters.FilterSet):
    category = filters.ModelChoiceFilter(field_name='category', queryset=FieldOfActivity.objects.all())
    province = filters.ModelChoiceFilter(field_name='province', queryset=Province.objects.all())
    type_of_cooperation = filters.ChoiceFilter(field_name='type_of_cooperation', choices=Ad.TYPE_OF_COOPERATION)
    work_experience = filters.ChoiceFilter(field_name='work_experience', choices=Ad.WORK_EXPERIENCE)
    salary = filters.ChoiceFilter(field_name='salary', choices=Ad.SALARY)

    class Meta:
        model = Ad
        fields = ['category', 'province', 'type_of_cooperation', 'salary']
