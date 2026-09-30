from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(
        name="Prediction",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("approved", models.BooleanField()),
            ("probability", models.FloatField()),
            ("applicant_name", models.CharField(blank=True, max_length=120)),
            ("summary", models.JSONField(default=dict)),
        ],
        options={"ordering": ["-created_at"]},
    )]
