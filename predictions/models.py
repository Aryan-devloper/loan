from django.db import models


class Prediction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField()
    probability = models.FloatField()
    applicant_name = models.CharField(max_length=120, blank=True)
    summary = models.JSONField(default=dict)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        status = "Approved" if self.approved else "Needs review"
        return f"{status} - {self.created_at:%Y-%m-%d %H:%M}"
