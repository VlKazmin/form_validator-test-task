from django.contrib import admin
from .models import FormTemplate


@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "date", "text")
    search_fields = ("name",)
