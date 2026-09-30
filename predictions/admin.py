from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "applicant_name", "approved", "probability")
    list_filter = ("approved", "created_at")
    readonly_fields = ("created_at",)
