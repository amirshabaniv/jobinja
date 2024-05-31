from django.contrib import admin

from .models import Ad, Skill, Resume, Save


admin.site.register(Skill)

admin.site.register(Save)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    raw_id_fields = ('job_seeker', 'ad')

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    raw_id_fields = ('skill', 'company')

