from rest_framework import serializers
from hospital.models import Hospital_Information, Patient, User
from doctor.models import (
    Doctor_Information, Appointment, Prescription,
    Prescription_medicine, Prescription_test, Report,
    Doctor_review, Education, Experience
)

# ─────────────────────────────────────────────
# USER
# ─────────────────────────────────────────────
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'is_patient', 'is_doctor', 'is_hospital_admin',
                  'is_pharmacist', 'login_status']


# ─────────────────────────────────────────────
# HOSPITAL
# ─────────────────────────────────────────────
class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital_Information
        fields = '__all__'


# ─────────────────────────────────────────────
# PATIENT
# ─────────────────────────────────────────────
class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'


# ─────────────────────────────────────────────
# DOCTOR
# ─────────────────────────────────────────────
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    user         = UserSerializer(read_only=True)
    hospital_name = HospitalSerializer(read_only=True)
    education_set = EducationSerializer(many=True, read_only=True)
    experience_set = ExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor_Information
        fields = '__all__'


# ─────────────────────────────────────────────
# APPOINTMENT
# ─────────────────────────────────────────────
class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name  = serializers.CharField(source='doctor.name', read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'


# ─────────────────────────────────────────────
# PRESCRIPTION
# ─────────────────────────────────────────────
class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription_medicine
        fields = '__all__'


class PrescriptionTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription_test
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    doctor_name   = serializers.CharField(source='doctor.name', read_only=True)
    patient_name  = serializers.CharField(source='patient.name', read_only=True)
    medicines     = PrescriptionMedicineSerializer(
        source='prescription_medicine_set', many=True, read_only=True)
    tests         = PrescriptionTestSerializer(
        source='prescription_test_set', many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'


# ─────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────
class ReportSerializer(serializers.ModelSerializer):
    doctor_name  = serializers.CharField(source='doctor.name', read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Report
        fields = '__all__'


# ─────────────────────────────────────────────
# DOCTOR REVIEW
# ─────────────────────────────────────────────
class DoctorReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Doctor_review
        fields = '__all__'
