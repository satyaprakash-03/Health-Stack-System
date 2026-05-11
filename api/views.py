from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    HospitalSerializer, PatientSerializer, DoctorSerializer,
    AppointmentSerializer, PrescriptionSerializer, ReportSerializer,
    DoctorReviewSerializer, UserSerializer
)
from hospital.models import Hospital_Information, Patient, User
from doctor.models import (
    Doctor_Information, Appointment, Prescription, Report, Doctor_review
)


# ══════════════════════════════════════════════════════════════
# ROOT — list all available API routes
# ══════════════════════════════════════════════════════════════
@api_view(['GET'])
def getRoutes(request):
    routes = [
        # Auth (JWT)
        {'POST': '/api/users/token/'},
        {'POST': '/api/users/token/refresh/'},

        # Hospital
        {'GET':  '/api/hospital/'},
        {'GET':  '/api/hospital/<id>/'},

        # Doctors
        {'GET':  '/api/doctors/'},
        {'GET':  '/api/doctors/<id>/'},

        # Patients
        {'GET':  '/api/patients/'},
        {'GET':  '/api/patients/<id>/'},

        # Appointments
        {'GET':  '/api/appointments/'},
        {'GET':  '/api/appointments/<id>/'},
        {'GET':  '/api/appointments/doctor/<doctor_id>/'},
        {'GET':  '/api/appointments/patient/<patient_id>/'},

        # Prescriptions
        {'GET':  '/api/prescriptions/patient/<patient_id>/'},
        {'GET':  '/api/prescriptions/<id>/'},

        # Reports
        {'GET':  '/api/reports/patient/<patient_id>/'},

        # Doctor Reviews
        {'GET':  '/api/reviews/doctor/<doctor_id>/'},

        # Users (admin only)
        {'GET':  '/api/users/'},
    ]
    return Response(routes)


# ══════════════════════════════════════════════════════════════
# HOSPITAL
# ══════════════════════════════════════════════════════════════
@api_view(['GET'])
def getHospitals(request):
    """Return all hospitals."""
    hospitals = Hospital_Information.objects.all()
    serializer = HospitalSerializer(hospitals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getHospitalProfile(request, pk):
    """Return a single hospital by ID."""
    try:
        hospital = Hospital_Information.objects.get(hospital_id=pk)
    except Hospital_Information.DoesNotExist:
        return Response({'error': 'Hospital not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = HospitalSerializer(hospital, many=False)
    return Response(serializer.data)


# ══════════════════════════════════════════════════════════════
# DOCTORS
# ══════════════════════════════════════════════════════════════
@api_view(['GET'])
def getDoctors(request):
    """Return all approved/active doctors."""
    doctors = Doctor_Information.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getDoctorProfile(request, pk):
    """Return a single doctor by ID."""
    try:
        doctor = Doctor_Information.objects.get(doctor_id=pk)
    except Doctor_Information.DoesNotExist:
        return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DoctorSerializer(doctor, many=False)
    return Response(serializer.data)


# ══════════════════════════════════════════════════════════════
# PATIENTS
# ══════════════════════════════════════════════════════════════
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPatients(request):
    """Return all patients (auth required)."""
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPatientProfile(request, pk):
    """Return a single patient by ID."""
    try:
        patient = Patient.objects.get(patient_id=pk)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PatientSerializer(patient, many=False)
    return Response(serializer.data)


# ══════════════════════════════════════════════════════════════
# APPOINTMENTS
# ══════════════════════════════════════════════════════════════
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAppointments(request):
    """Return all appointments."""
    appointments = Appointment.objects.all().order_by('-date')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAppointmentDetail(request, pk):
    """Return a single appointment by ID."""
    try:
        appointment = Appointment.objects.get(id=pk)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAppointmentsByDoctor(request, doctor_id):
    """Return all appointments for a specific doctor."""
    appointments = Appointment.objects.filter(doctor__doctor_id=doctor_id).order_by('-date')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAppointmentsByPatient(request, patient_id):
    """Return all appointments for a specific patient."""
    appointments = Appointment.objects.filter(patient__patient_id=patient_id).order_by('-date')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# ══════════════════════════════════════════════════════════════
# PRESCRIPTIONS
# ══════════════════════════════════════════════════════════════
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPrescriptionsByPatient(request, patient_id):
    """Return all prescriptions for a specific patient."""
    prescriptions = Prescription.objects.filter(patient__patient_id=patient_id)
    serializer = PrescriptionSerializer(prescriptions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPrescriptionDetail(request, pk):
    """Return a single prescription by ID."""
    try:
        prescription = Prescription.objects.get(prescription_id=pk)
    except Prescription.DoesNotExist:
        return Response({'error': 'Prescription not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PrescriptionSerializer(prescription)
    return Response(serializer.data)


# ══════════════════════════════════════════════════════════════
# REPORTS
# ══════════════════════════════════════════════════════════════
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReportsByPatient(request, patient_id):
    """Return all lab reports for a specific patient."""
    reports = Report.objects.filter(patient__patient_id=patient_id)
    serializer = ReportSerializer(reports, many=True)
    return Response(serializer.data)


# ══════════════════════════════════════════════════════════════
# DOCTOR REVIEWS
# ══════════════════════════════════════════════════════════════
@api_view(['GET'])
def getDoctorReviews(request, doctor_id):
    """Return all reviews for a specific doctor."""
    reviews = Doctor_review.objects.filter(doctor__doctor_id=doctor_id)
    serializer = DoctorReviewSerializer(reviews, many=True)
    return Response(serializer.data)


# ══════════════════════════════════════════════════════════════
# USERS  (admin only)
# ══════════════════════════════════════════════════════════════
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    """Return all users — admin only."""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
