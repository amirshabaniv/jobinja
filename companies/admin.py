from django.contrib import admin

from .models import Company, FieldOfActivity, Province, City


admin.site.register(FieldOfActivity)

admin.site.register(Province)

admin.site.register(City)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    raw_id_fields = ('province', 'city', 'field_of_activity')