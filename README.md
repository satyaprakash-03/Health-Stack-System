# HealthStack System 

HealthStack System is a Django-based healthcare management platform for connecting patients, doctors, hospitals, hospital administrators, lab workers, and pharmacists in one place. The application supports hospital discovery, doctor registration and approval, appointment booking, prescriptions, lab reports, pharmacy ordering, online payments, email notifications, PDF generation, chat, and an AI symptom checker.

This project was built as a Software Engineering project for B.Sc. Computer Science and Engineering.

## Features

- Role-based accounts for patients, doctors, hospital admins, lab workers, and pharmacists.
- Patient registration, login, dashboard, profile management, and password reset.
- Hospital search, hospital profiles, departments, services, and doctor listings.
- Doctor registration with certificate upload and hospital admin approval workflow.
- Appointment booking, appointment approval/rejection, and email confirmation.
- Doctor-patient chat.
- Prescription creation, viewing, deletion, and PDF download.
- Lab test creation, test cart, report creation, report viewing, and PDF download.
- Pharmacy shop with medicine search, product pages, cart, checkout, and order tracking.
- SSLCommerz payment gateway integration for appointments, lab tests, and pharmacy orders.
- Contact, FAQ, support, privacy policy, and terms pages.
- AI symptom checker and AI chat endpoint.
- REST API endpoints for hospitals and JWT authentication.

## Tech Stack

- Python
- Django 4.1
- Django REST Framework
- SQLite
- Bootstrap, HTML, CSS, JavaScript, Ajax
- Pillow for image uploads
- xhtml2pdf and ReportLab for PDF generation
- django-environ and python-decouple for environment configuration
- django-widget-tweaks for form rendering
- django-debug-toolbar for development debugging
- SSLCommerz payment gateway
- SMTP email integration

## Project Structure

```text
Health Stack System/
|-- api/                # REST API endpoints
|-- ChatApp/            # Doctor-patient chat
|-- doctor/             # Doctor, appointment, prescription, report logic
|-- healthstack/        # Django project settings and root URLs
|-- hospital/           # Home, patient, hospital, contact, symptom checker logic
|-- hospital_admin/     # Hospital admin, lab worker, pharmacist admin workflows
|-- pharmacy/           # Medicine shop, cart, and checkout
|-- sslcommerz/         # Payment gateway integration
|-- static/             # CSS, JavaScript, images, uploaded media
|-- templates/          # Django templates
|-- manage.py
|-- requirements.txt
`-- .env.example
```

## Requirements

- Python 3.10 or newer recommended
- pip
- virtualenv or Python venv
- SQLite, included with Python

## Environment Variables

Create a `.env` file in the project root using `.env.example` as a starting point:

```env
DEBUG=True
SECRET_KEY="your-django-secret-key"

SMTP_HOST=""
SMTP_PORT=
SMTP_USER=""
SMTP_PASSWORD=""

STORE_ID=""
STORE_PASSWORD=""
STORE_NAME=""

EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""
```

Notes:

- `SECRET_KEY` is required by Django.
- `STORE_ID`, `STORE_PASSWORD`, and `STORE_NAME` are used for SSLCommerz payments.
- SMTP and Gmail values are used for email notifications and password reset emails.
- Do not commit your real `.env` file.

## Installation

1. Clone or open the project folder.

2. Create a virtual environment.

```bash
python -m venv venv
```

3. Activate the virtual environment.

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

4. Install dependencies.

```bash
pip install -r requirements.txt
```

5. Install Simple JWT if it is not already installed.

```bash
pip install djangorestframework-simplejwt
```

6. Create and configure the `.env` file.

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

7. Run database migrations.

```bash
python manage.py migrate
```

8. Create a superuser.

```bash
python manage.py createsuperuser
```

9. Start the development server.

```bash
python manage.py runserver
```

Open the app at:

```text
http://127.0.0.1:8000/
```

## Main URLs

| Area | URL |
| --- | --- |
| Home | `/` |
| Django admin | `/admin/` |
| Login | `/login/` |
| Patient registration | `/patient-register/` |
| Patient dashboard | `/patient-dashboard/` |
| Doctor login | `/doctor/` |
| Doctor dashboard | `/doctor/doctor-dashboard/` |
| Hospital admin login | `/hospital_admin/` |
| Hospital admin dashboard | `/hospital_admin/admin-dashboard/` |
| Pharmacy shop | `/pharmacy/shop/` |
| Cart | `/pharmacy/cart/` |
| Chat | `/chat/` |
| Symptom checker | `/symptom-checker/` |
| API routes | `/api/` |
| JWT token | `/api/users/token/` |
| JWT refresh | `/api/users/token/refresh/` |

## User Roles

### Patient

- Search hospitals, departments, and doctors.
- Book appointments with doctors.
- Pay for appointments and lab tests.
- View prescriptions and download prescription PDFs.
- View lab reports and download report PDFs.
- Chat with appointed doctors.
- Review doctors.
- Purchase medicines from the pharmacy.

### Doctor

- Register and upload certificate for hospital approval.
- Manage doctor profile, education, and experience.
- Accept or reject patient appointments.
- View patient profiles.
- Create prescriptions.
- View prescriptions and reports.
- Chat with appointed patients.

### Hospital Admin

- Manage hospital profile and hospital information.
- Approve or reject doctor registrations.
- Manage departments, specializations, and services.
- Manage lab workers and pharmacists.
- Manage tests, reports, appointments, invoices, and medicine records.

### Lab Worker

- Access lab worker dashboard.
- Create patient reports.
- Create and manage hospital tests.
- View report history.

### Pharmacist

- Access pharmacist dashboard.
- Add, edit, delete, and manage medicines.
- Handle medicine listings used by the pharmacy shop.

## API Endpoints

| Endpoint | Description |
| --- | --- |
| `/api/` | API route overview |
| `/api/hospital/` | List hospitals |
| `/api/hospital/<id>/` | Hospital profile detail |
| `/api/users/token/` | JWT access and refresh token |
| `/api/users/token/refresh/` | Refresh JWT token |

## Screenshots

Project screenshots are stored under:

```text
static/images/Project Image/
```

Available screenshot folders include:

- `Home page`
- `Patient`
- `Doctor`
- `Hospital Admin`
- `Medical Shop`
- `Pharmacist`

## Development Notes

- The project uses a custom user model: `hospital.User`.
- Uploaded media is stored under `static/images/` through `MEDIA_ROOT`.
- The default database is SQLite: `db.sqlite3`.
- Debug toolbar is enabled for local development at `/__debug__/`.
- `ALLOWED_HOSTS` is configured in `healthstack/settings.py`; update it for your local or deployment environment.
- Run migrations after changing models:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Common Commands

```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## Contributors

- Satyaprakash Prajapati
- Shivam Dubey
- Swapnil Tripathi

## License

No license file is currently included in this working tree. Add a `LICENSE` file before distributing or publishing the project.
