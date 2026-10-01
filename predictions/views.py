from functools import lru_cache
from pathlib import Path
import joblib
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from .forms import LoanPredictionForm
from .models import Prediction

MODEL_PATH = Path(settings.BASE_DIR) / "model.joblib"


@lru_cache(maxsize=1)
def load_pipeline():
    return joblib.load(MODEL_PATH)


def dashboard(request):
    history = Prediction.objects.all()[:6]
    stats = {
        "total": Prediction.objects.count(),
        "approved": Prediction.objects.filter(approved=True).count(),
        "review": Prediction.objects.filter(approved=False).count(),
    }
    return render(request, "predictions/dashboard.html", {"history": history, "stats": stats})


def predict(request):
    result = None
    form = LoanPredictionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if not MODEL_PATH.exists():
            form.add_error(None, "The model is not trained yet. Run: python train_model.py")
        else:
            values = form.cleaned_data.copy()
            applicant_name = values.pop("applicant_name", "")
            features = pd.DataFrame([values])
            pipeline = load_pipeline()
            approved = bool(pipeline.predict(features)[0])
            probabilities = pipeline.predict_proba(features)[0]
            probability = float(probabilities[1]) if len(probabilities) > 1 else float(approved)
            prediction = Prediction.objects.create(
                approved=approved,
                probability=probability,
                applicant_name=applicant_name,
                summary={"loan_amount": values["Loan_Amount"], "credit_score": values["Credit_Score"]},
            )
            result = {"approved": approved, "probability": round(probability * 100, 1), "prediction": prediction}
            form = LoanPredictionForm()
    fields = list(form)
    context = {
        "form": form,
        "result": result,
        "profile_fields": fields[:9],
        "financial_fields": fields[9:19],
        "loan_fields": fields[19:],
    }
    return render(request, "predictions/predict.html", context)
