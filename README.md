# Lendwise Django Loan Approval App

A complete Django conversion of the loan approval notebook. It trains a production-style scikit-learn pipeline with numeric imputation, one-hot encoding for categorical fields, and a balanced Random Forest classifier. The web UI provides a responsive applicant form, recommendation confidence, and saved assessment history.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python train_model.py
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

The training script defaults to the project-local `loan_approval.csv`, saves `model.joblib`, and prints a held-out classification report. If the CSV is elsewhere, pass its path as the first argument. The admin screen is available at `/admin/` after creating a superuser with `python manage.py createsuperuser`.

## Deploying online

This is a Django server application and cannot run directly on Netlify's static hosting. Deploy it on Render, Railway, or PythonAnywhere. A Render blueprint is included in `render.yaml`; it installs dependencies, trains the model from the committed CSV, runs migrations, collects static files, and starts Gunicorn. Set `DJANGO_SECRET_KEY` to a secure value in the hosting dashboard.
