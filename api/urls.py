from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # ── Root ──────────────────────────────────────────────────
    path('', views.getRoutes, name='api-routes'),

    # ── JWT Auth ──────────────────────────────────────────────
    path('users/token/',         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(),    name='token_refresh'),

    # ── Users (admin only) ────────────────────────────────────
    path('users/', views.getUsers, name='api-users'),

    # ── Hospital ──────────────────────────────────────────────
    path('hospital/',      views.getHospitals,      name='api-hospitals'),
    path('hospital/<int:pk>/', views.getHospitalProfile, name='api-hospital-detail'),

    # ── Doctors ───────────────────────────────────────────────
    path('doctors/',           views.getDoctors,       name='api-doctors'),
    path('doctors/<int:pk>/',  views.getDoctorProfile, name='api-doctor-detail'),

    # ── Patients ──────────────────────────────────────────────
    path('patients/',           views.getPatients,       name='api-patients'),
    path('patients/<int:pk>/',  views.getPatientProfile, name='api-patient-detail'),

    # ── Appointments ──────────────────────────────────────────
    path('appointments/',                              views.getAppointments,          name='api-appointments'),
    path('appointments/<int:pk>/',                     views.getAppointmentDetail,     name='api-appointment-detail'),
    path('appointments/doctor/<int:doctor_id>/',       views.getAppointmentsByDoctor,  name='api-appointments-doctor'),
    path('appointments/patient/<int:patient_id>/',     views.getAppointmentsByPatient, name='api-appointments-patient'),

    # ── Prescriptions ─────────────────────────────────────────
    path('prescriptions/<int:pk>/',                    views.getPrescriptionDetail,    name='api-prescription-detail'),
    path('prescriptions/patient/<int:patient_id>/',    views.getPrescriptionsByPatient,name='api-prescriptions-patient'),

    # ── Reports ───────────────────────────────────────────────
    path('reports/patient/<int:patient_id>/',          views.getReportsByPatient,      name='api-reports-patient'),

    # ── Doctor Reviews ────────────────────────────────────────
    path('reviews/doctor/<int:doctor_id>/',            views.getDoctorReviews,         name='api-doctor-reviews'),
]
