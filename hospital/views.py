import email
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, PatientForm, PasswordResetForm
from hospital.models import Hospital_Information, User, Patient 
from doctor.models import Test, testCart, testOrder
from hospital_admin.models import hospital_department, specialization, service, Test_Information
from django.views.decorators.cache import cache_control
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import datetime
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.template.loader import get_template
from xhtml2pdf import pisa
from .utils import searchDoctors, searchHospitals, searchDepartmentDoctors, paginateHospitals
from .models import Patient, User
from doctor.models import Doctor_Information, Appointment,Report, Specimen, Test, Prescription, Prescription_medicine, Prescription_test
from sslcommerz.models import Payment
from django.db.models import Q, Count
import re
from io import BytesIO
from urllib import response
from django.core.mail import BadHeaderError, send_mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def hospital_home(request):
    # .order_by('-created_at')[:6]
    doctors = Doctor_Information.objects.filter(register_status='Accepted')
    hospitals = Hospital_Information.objects.all()
    # Latest published blogs for homepage
    from blog.models import BlogPost
    latest_blogs = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:6]
    context = {'doctors': doctors, 'hospitals': hospitals, 'latest_blogs': latest_blogs}
    return render(request, 'index-2.html', context)

@csrf_exempt
@login_required(login_url="login")
def change_password(request,pk):
    patient = Patient.objects.get(user_id=pk)
    context={"patient":patient}
    if request.method == "POST":
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]
        if new_password == confirm_password:
            
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request,"Password Changed Successfully")
            return redirect("patient-dashboard")
        else:
            messages.error(request,"New Password and Confirm Password is not same")
            return redirect("change-password",pk)
    return render(request, 'change-password.html',context)


def add_billing(request):
    return render(request, 'add-billing.html')

def appointments(request):
    return render(request, 'appointments.html')

def edit_billing(request):
    return render(request, 'edit-billing.html')

def edit_prescription(request):
    return render(request, 'edit-prescription.html')

# def forgot_password(request):
#     return render(request, 'forgot-password.html')

@csrf_exempt
def resetPassword(request):
    form = PasswordResetForm()

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = user.email
       
            subject = "Password Reset Requested"
            # email_template_name = "password_reset_email.txt"
            values = {
				"email":user.email,
				'domain':'127.0.0.1:8000',
				'site_name': 'Website',
				"uid": urlsafe_base64_encode(force_bytes(user.pk)),
				"user": user,
				'token': default_token_generator.make_token(user),
				'protocol': 'http',
			}

            html_message = render_to_string('mail_template.html', {'values': values})
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(subject, plain_message, 'admin@example.com',  [user.email], html_message=html_message, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect ("password_reset_done")

    context = {'form': form}
    return render(request, 'reset_password.html', context)
    
    
def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def about_us(request):
    return render(request, 'about-us.html')

@csrf_exempt
@login_required(login_url="login")
def chat(request, pk):
    patient = Patient.objects.get(user_id=pk)
    doctors = Doctor_Information.objects.all()

    context = {'patient': patient, 'doctors': doctors}
    return render(request, 'chat.html', context)

@csrf_exempt
@login_required(login_url="login")
def chat_doctor(request):
    if request.user.is_doctor:
        doctor = Doctor_Information.objects.get(user=request.user)
        patients = Patient.objects.all()
        
    context = {'patients': patients, 'doctor': doctor}
    return render(request, 'chat-doctor.html', context)

@csrf_exempt     
@login_required(login_url="login")
def pharmacy_shop(request):
    return render(request, 'pharmacy/shop.html')

@csrf_exempt
def login_user(request):
    page = 'patient_login'
    if request.method == 'GET':
        return render(request, 'patient-login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_patient:   
                messages.success(request, 'User Logged in Successfully')    
                return redirect('patient-dashboard')
            else:
                messages.error(request, 'Invalid credentials. Not a Patient')
                return redirect('logout')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'patient-login.html')

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):
    logout(request)
    messages.success(request, 'User Logged out')
    return redirect('login')

@csrf_exempt
def patient_register(request):
    page = 'patient-register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save(commit=False) # commit=False --> don't save to database yet (we have a chance to modify object)
            user.is_patient = True
            # user.username = user.username.lower()  # lowercase username
            user.save()
            messages.success(request, 'Patient account was created!')

            # After user is created, we can log them in --> login(request, user)
            return redirect('login')

        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'patient-register.html', context)

@csrf_exempt
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def patient_dashboard(request):
    if request.user.is_patient:
        # patient = Patient.objects.get(user_id=pk)
        patient = Patient.objects.get(user=request.user)
        report = Report.objects.filter(patient=patient)
        prescription = Prescription.objects.filter(patient=patient).order_by('-prescription_id')
        appointments = Appointment.objects.filter(patient=patient).filter(Q(appointment_status='pending') | Q(appointment_status='confirmed'))
        payments = Payment.objects.filter(patient=patient).filter(appointment__in=appointments).filter(payment_type='appointment').filter(status='VALID')
        context = {'patient': patient, 'appointments': appointments, 'payments': payments,'report':report,'prescription':prescription}
    else:
        return redirect('logout')
        
    return render(request, 'patient-dashboard.html', context)


# def profile_settings(request):
#     if request.user.is_patient:
#         # patient = Patient.objects.get(user_id=pk)
#         patient = Patient.objects.get(user=request.user)
#         form = PatientForm(instance=patient)  

#         if request.method == 'POST':
#             form = PatientForm(request.POST, request.FILES,instance=patient)  
#             if form.is_valid():
#                 form.save()
#                 return redirect('patient-dashboard')
#             else:
#                 form = PatientForm()
#     else:
#         redirect('logout')

#     context = {'patient': patient, 'form': form}
#     return render(request, 'profile-settings.html', context)

@csrf_exempt
@login_required(login_url="login")
def profile_settings(request):
    if request.user.is_patient:
        # patient = Patient.objects.get(user_id=pk)
        patient = Patient.objects.get(user=request.user)
        old_featured_image = patient.featured_image
        
        if request.method == 'GET':
            context = {'patient': patient}
            return render(request, 'profile-settings.html', context)
        elif request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = old_featured_image
                
            name = request.POST.get('name')
            dob = request.POST.get('dob')
            age = request.POST.get('age')
            blood_group = request.POST.get('blood_group')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            nid = request.POST.get('nid')
            history = request.POST.get('history')
            
            patient.name = name
            patient.age = age
            patient.phone_number = phone_number
            patient.address = address
            patient.blood_group = blood_group
            patient.history = history
            patient.dob = dob
            patient.nid = nid
            patient.featured_image = featured_image
            
            patient.save()
            
            messages.success(request, 'Profile Settings Changed!')
            
            return redirect('patient-dashboard')
    else:
        redirect('logout')  
        
@csrf_exempt
@login_required(login_url="login")
def search(request):
    if request.user.is_authenticated and request.user.is_patient:
        # patient = Patient.objects.get(user_id=pk)
        patient = Patient.objects.get(user=request.user)
        doctors = Doctor_Information.objects.filter(register_status='Accepted')
        
        doctors, search_query = searchDoctors(request)
        context = {'patient': patient, 'doctors': doctors, 'search_query': search_query}
        return render(request, 'search.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')    
    

def checkout_payment(request):
    return render(request, 'checkout.html')

@csrf_exempt
@login_required(login_url="login")
def multiple_hospital(request):
    
    if request.user.is_authenticated: 
        
        if request.user.is_patient:
            # patient = Patient.objects.get(user_id=pk)
            patient = Patient.objects.get(user=request.user)
            doctors = Doctor_Information.objects.all()
            hospitals = Hospital_Information.objects.all()
            
            hospitals, search_query = searchHospitals(request)
            
            # PAGINATION ADDED TO MULTIPLE HOSPITALS
            custom_range, hospitals = paginateHospitals(request, hospitals, 3)
        
            context = {'patient': patient, 'doctors': doctors, 'hospitals': hospitals, 'search_query': search_query, 'custom_range': custom_range}
            return render(request, 'multiple-hospital.html', context)
        
        elif request.user.is_doctor:
            doctor = Doctor_Information.objects.get(user=request.user)
            hospitals = Hospital_Information.objects.all()
            
            hospitals, search_query = searchHospitals(request)
            
            context = {'doctor': doctor, 'hospitals': hospitals, 'search_query': search_query}
            return render(request, 'multiple-hospital.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 
    
@csrf_exempt    
@login_required(login_url="login")
def hospital_profile(request, pk):
    
    if request.user.is_authenticated: 
        
        if request.user.is_patient:
            patient = Patient.objects.get(user=request.user)
            doctors = Doctor_Information.objects.all()
            hospitals = Hospital_Information.objects.get(hospital_id=pk)
        
            departments = hospital_department.objects.filter(hospital=hospitals)
            specializations = specialization.objects.filter(hospital=hospitals)
            services = service.objects.filter(hospital=hospitals)
            
            # department_list = None
            # for d in departments:
            #     vald = d.hospital_department_name
            #     vald = re.sub("'", "", vald)
            #     vald = vald.replace("[", "")
            #     vald = vald.replace("]", "")
            #     vald = vald.replace(",", "")
            #     department_list = vald.split()
            
            context = {'patient': patient, 'doctors': doctors, 'hospitals': hospitals, 'departments': departments, 'specializations': specializations, 'services': services}
            return render(request, 'hospital-profile.html', context)
        
        elif request.user.is_doctor:
           
            doctor = Doctor_Information.objects.get(user=request.user)
            hospitals = Hospital_Information.objects.get(hospital_id=pk)
            
            departments = hospital_department.objects.filter(hospital=hospitals)
            specializations = specialization.objects.filter(hospital=hospitals)
            services = service.objects.filter(hospital=hospitals)
            
            context = {'doctor': doctor, 'hospitals': hospitals, 'departments': departments, 'specializations': specializations, 'services': services}
            return render(request, 'hospital-profile.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 
    
    
def data_table(request):
    return render(request, 'data-table.html')

@csrf_exempt
@login_required(login_url="login")
def hospital_department_list(request, pk):
    if request.user.is_authenticated: 
        
        if request.user.is_patient:
            # patient = Patient.objects.get(user_id=pk)
            patient = Patient.objects.get(user=request.user)
            doctors = Doctor_Information.objects.all()
            
            hospitals = Hospital_Information.objects.get(hospital_id=pk)
            departments = hospital_department.objects.filter(hospital=hospitals)
        
            context = {'patient': patient, 'doctors': doctors, 'hospitals': hospitals, 'departments': departments}
            return render(request, 'hospital-department.html', context)
        
        elif request.user.is_doctor:
            doctor = Doctor_Information.objects.get(user=request.user)
            hospitals = Hospital_Information.objects.get(hospital_id=pk)
            departments = hospital_department.objects.filter(hospital=hospitals)
            
            context = {'doctor': doctor, 'hospitals': hospitals, 'departments': departments}
            return render(request, 'hospital-department.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'patient-login.html')

@csrf_exempt
@login_required(login_url="login")
def hospital_doctor_list(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
        # patient = Patient.objects.get(user_id=pk)
        patient = Patient.objects.get(user=request.user)
        departments = hospital_department.objects.get(hospital_department_id=pk)
        doctors = Doctor_Information.objects.filter(department_name=departments)
        
        doctors, search_query = searchDepartmentDoctors(request, pk)
        
        context = {'patient': patient, 'department': departments, 'doctors': doctors, 'search_query': search_query, 'pk_id': pk}
        return render(request, 'hospital-doctor-list.html', context)

    elif request.user.is_authenticated and request.user.is_doctor:
        # patient = Patient.objects.get(user_id=pk)
        
        doctor = Doctor_Information.objects.get(user=request.user)
        departments = hospital_department.objects.get(hospital_department_id=pk)
        
        doctors = Doctor_Information.objects.filter(department_name=departments)
        doctors, search_query = searchDepartmentDoctors(request, pk)
        
        context = {'doctor':doctor, 'department': departments, 'doctors': doctors, 'search_query': search_query, 'pk_id': pk}
        return render(request, 'hospital-doctor-list.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')   
    


@csrf_exempt
@login_required(login_url="login")
def hospital_doctor_register(request, pk):
    if request.user.is_authenticated: 
        
        if request.user.is_doctor:
            doctor = Doctor_Information.objects.get(user=request.user)
            hospitals = Hospital_Information.objects.get(hospital_id=pk)
            
            departments = hospital_department.objects.filter(hospital=hospitals)
            specializations = specialization.objects.filter(hospital=hospitals)
            
            if request.method == 'POST':
                if 'certificate_image' in request.FILES:
                    certificate_image = request.FILES['certificate_image']
                else:
                    certificate_image = "doctors_certificate/default.png"
                
                department_id_selected = request.POST.get('department_radio')
                specialization_id_selected = request.POST.get('specialization_radio')
                
                department_chosen = hospital_department.objects.get(hospital_department_id=department_id_selected)
                specialization_chosen = specialization.objects.get(specialization_id=specialization_id_selected)
                
                doctor.department_name = department_chosen
                doctor.specialization = specialization_chosen
                doctor.register_status = 'Pending'
                doctor.certificate_image = certificate_image
                
                doctor.save()
                
                messages.success(request, 'Hospital Registration Request Sent')
                
                return redirect('doctor-dashboard')
                
                 
            context = {'doctor': doctor, 'hospitals': hospitals, 'departments': departments, 'specializations': specializations}
            return render(request, 'hospital-doctor-register.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'doctor-login.html')
    
   
def testing(request):
    # hospitals = Hospital_Information.objects.get(hospital_id=1)
    test = "test"
    context = {'test': test}
    return render(request, 'testing.html', context)

@csrf_exempt
@login_required(login_url="login")
def view_report(request,pk):
    if request.user.is_patient:
        patient = Patient.objects.get(user=request.user)
        report = Report.objects.filter(report_id=pk)
        specimen = Specimen.objects.filter(report__in=report)
        test = Test.objects.filter(report__in=report)

        # current_date = datetime.date.today()
        context = {'patient':patient,'report':report,'test':test,'specimen':specimen}
        return render(request, 'view-report.html',context)
    else:
        return redirect('logout') 


# removed duplicate stub test_cart — real test_cart with pk arg is defined below

@csrf_exempt
@login_required(login_url="login")
def test_single(request,pk):
     if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        prescription_test_obj = Prescription_test.objects.get(test_id=pk)
        carts = testCart.objects.filter(user=request.user, purchased=False)
        
        context = {'patient': patient, 'carts': carts, 'prescription_test_obj': prescription_test_obj}
        return render(request, 'test-cart.html',context)
     else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="login")
def test_add_to_cart(request, pk, pk2):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        test_information = Test_Information.objects.get(test_id=pk2)
        prescription = Prescription.objects.filter(prescription_id=pk)

        item = get_object_or_404(Prescription_test, test_info_id=pk2,prescription_id=pk)
        order_item = testCart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_qs = testOrder.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]
            order.orderitems.add(order_item[0])
            # messages.info(request, "This test is added to your cart!")
            return redirect("prescription-view", pk=pk)
        else:
            order = testOrder(user=request.user)
            order.save()
            order.orderitems.add(order_item[0])
            return redirect("prescription-view", pk=pk)

        context = {'patient': patient,'prescription_test': prescription_tests,'prescription':prescription,'prescription_medicine':prescription_medicine,'test_information':test_information}
        return render(request, 'prescription-view.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="login")
def test_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
        # prescription = Prescription.objects.filter(prescription_id=pk)
        
        prescription = Prescription.objects.filter(prescription_id=pk)
        
        patient = Patient.objects.get(user=request.user)
        prescription_test = Prescription_test.objects.all()
        test_carts = testCart.objects.filter(user=request.user, purchased=False)
        test_orders = testOrder.objects.filter(user=request.user, ordered=False)
        
        if test_carts.exists() and test_orders.exists():
            test_order = test_orders[0]
            
            context = {'test_carts': test_carts,'test_order': test_order, 'patient': patient, 'prescription_test':prescription_test, 'prescription_id':pk}
            return render(request, 'test-cart.html', context)
        else:
            # messages.warning(request, "You don't have any test in your cart!")
            context = {'patient': patient,'prescription_test':prescription_test}
            return render(request, 'prescription-view.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'patient-login.html') 

@csrf_exempt
@login_required(login_url="login")
def test_remove_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
        item = Prescription_test.objects.get(test_id=pk)

        patient = Patient.objects.get(user=request.user)
        prescription = Prescription.objects.filter(prescription_id=pk)
        prescription_medicine = Prescription_medicine.objects.filter(prescription__in=prescription)
        prescription_test = Prescription_test.objects.filter(prescription__in=prescription)
        test_carts = testCart.objects.filter(user=request.user, purchased=False)
        
        # item = get_object_or_404(test, pk=pk)
        test_order_qs = testOrder.objects.filter(user=request.user, ordered=False)
        if test_order_qs.exists():
            test_order = test_order_qs[0]
            if test_order.orderitems.filter(item=item).exists():
                test_order_item = testCart.objects.filter(item=item, user=request.user, purchased=False)[0]
                test_order.orderitems.remove(test_order_item)
                test_order_item.delete()
                # messages.warning(request, "This test was remove from your cart!")
                context = {'test_carts': test_carts,'test_order': test_order,'patient': patient,'prescription_id':pk}
                return render(request, 'test-cart.html', context)
            else:
                # messages.info(request, "This test was not in your cart")
                context = {'patient': patient,'test': item,'prescription':prescription,'prescription_medicine':prescription_medicine,'prescription_test':prescription_test}
                return render(request, 'prescription-view.html', context)
        else:
            # messages.info(request, "You don't have an active order")
            first_prescription = prescription.first()
            pk_val = first_prescription.prescription_id if first_prescription else 0
            return redirect('prescription-view', pk=pk_val)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'patient-login.html') 

@csrf_exempt
def prescription_view(request,pk):
      if request.user.is_patient:
        patient = Patient.objects.get(user=request.user)
        prescription = Prescription.objects.filter(prescription_id=pk)
        prescription_medicine = Prescription_medicine.objects.filter(prescription__in=prescription)
        prescription_test = Prescription_test.objects.filter(prescription__in=prescription)

        context = {'patient':patient,'prescription':prescription,'prescription_test':prescription_test,'prescription_medicine':prescription_medicine}
        return render(request, 'prescription-view.html',context)
      else:
         return redirect('logout') 

@csrf_exempt
def render_to_pdf(template_src, context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pres_pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pres_pdf.err:
        return HttpResponse(result.getvalue(),content_type="aplication/pres_pdf")
    return None


# def prescription_pdf(request,pk):
#  if request.user.is_patient:
#     patient = Patient.objects.get(user=request.user)
#     prescription = Prescription.objects.get(prescription_id=pk)
#     perscription_medicine = Perscription_medicine.objects.filter(prescription=prescription)
#     perscription_test = Perscription_test.objects.filter(prescription=prescription)
#     current_date = datetime.date.today()
#     context={'patient':patient,'current_date' : current_date,'prescription':prescription,'perscription_test':perscription_test,'perscription_medicine':perscription_medicine}
#     pdf=render_to_pdf('prescription_pdf.html', context)
#     if pdf:
#         response=HttpResponse(pdf, content_type='application/pdf')
#         content="inline; filename=report.pdf"
#         # response['Content-Disposition']= content
#         return response
#     return HttpResponse("Not Found")

@csrf_exempt
def prescription_pdf(request,pk):
 if request.user.is_patient:
    patient = Patient.objects.get(user=request.user)
    prescription = Prescription.objects.get(prescription_id=pk)
    prescription_medicine = Prescription_medicine.objects.filter(prescription=prescription)
    prescription_test = Prescription_test.objects.filter(prescription=prescription)
    # current_date = datetime.date.today()
    context={'patient':patient,'prescription':prescription,'prescription_test':prescription_test,'prescription_medicine':prescription_medicine}
    pres_pdf=render_to_pdf('prescription_pdf.html', context)
    if pres_pdf:
        response=HttpResponse(pres_pdf, content_type='application/pres_pdf')
        content="inline; filename=prescription.pdf"
        response['Content-Disposition']= content
        return response
    return HttpResponse("Not Found")

@csrf_exempt
@login_required(login_url="login")
def delete_prescription(request,pk):
    if request.user.is_authenticated and request.user.is_patient:
        prescription = Prescription.objects.get(prescription_id=pk)
        prescription.delete()
        messages.success(request, 'Prescription Deleted')
        return redirect('patient-dashboard')
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')

@csrf_exempt
@login_required(login_url="login")
def delete_report(request,pk):
    if request.user.is_authenticated and request.user.is_patient:
        report = Report.objects.get(report_id=pk)
        report.delete()
        messages.success(request, 'Report Deleted')
        return redirect('patient-dashboard')
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')

@csrf_exempt
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.login_status = True
    user.save()

@csrf_exempt
@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.login_status = False
    user.save()
    




def contact_us(request):
    from .models import ContactMessage
    from django.contrib import messages
    from django.core.mail import EmailMessage
    from django.conf import settings as django_settings

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        phone   = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', 'General Inquiry').strip()
        city    = request.POST.get('city', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            # 1. Save to database (always — even if email fails)
            ContactMessage.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, city=city, message=message
            )

            # 2. Send professional email notification to your Gmail
            email_subject = f'[HealthStack Contact] {subject} — from {name}'
            email_body = f"""Namaskar,

Aapko HealthStack website se ek naya contact message mila hai.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SENDER DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Name    : {name}
  Email   : {email}
  Phone   : {phone or 'Not provided'}
  City    : {city or 'Not provided'}
  Subject : {subject}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MESSAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Directly reply kar sakte hain — Reply-To: {email}
— HealthStack System (Automated Notification)
""".strip()

            try:
                # Use EmailMessage so reply_to header is properly set
                mail = EmailMessage(
                    subject   = email_subject,
                    body      = email_body,
                    from_email= django_settings.EMAIL_HOST_USER,
                    to        = ['satyaprakash.in33@gmail.com'],
                    reply_to  = [email],   # ✅ clicking Reply in Gmail goes to the user
                )
                mail.send(fail_silently=False)
                messages.success(
                    request,
                    f"Thank you {name}! Your message has been sent successfully. "
                    "We'll get back to you within 24 hours."
                )
            except Exception as e:
                # Email failed — but DB record is safe, so just warn
                messages.warning(
                    request,
                    "Message saved successfully! However, the email notification "
                    "could not be sent right now. We'll still review your message."
                )

    return render(request, 'footer_contact.html')


def faqs(request):
    return render(request, 'footer_faqs.html')

def support(request):
    return render(request, 'footer_support.html')

def terms(request):
    return render(request, 'footer_terms.html')


# ─────────────────────────────────────────────────────────────
#  AI SYMPTOM CHECKER
# ─────────────────────────────────────────────────────────────

import json

# Rule-based symptom knowledge base
SYMPTOM_DB = {
    "fever": {
        "condition": "Fever / Viral Infection",
        "causes": "Fever is usually caused by a viral or bacterial infection, flu, COVID-19, or inflammation.",
        "precautions": [
            "Stay hydrated — drink plenty of water and fluids.",
            "Rest adequately and avoid strenuous activity.",
            "Take paracetamol/acetaminophen to manage high temperature.",
            "Use a cool, damp cloth on forehead and wrists.",
            "Monitor temperature every 4 hours.",
        ],
        "see_doctor": "Consult a General Physician if fever exceeds 103°F (39.4°C), lasts more than 3 days, or is accompanied by a stiff neck or rash.",
        "specialist": "General Physician / Internal Medicine",
        "urgency": "⚠️ Moderate — see a doctor within 24–48 hours if fever persists.",
    },
    "cough": {
        "condition": "Cough / Respiratory Infection",
        "causes": "Cough can be due to the common cold, flu, allergies, asthma, bronchitis, or COVID-19.",
        "precautions": [
            "Drink warm liquids (honey-lemon tea, warm water).",
            "Use a humidifier or steam inhalation to soothe airways.",
            "Avoid cold drinks, dust, and smoke.",
            "Gargle with warm salt water to ease throat irritation.",
            "Cover your mouth while coughing to prevent spread.",
        ],
        "see_doctor": "See a doctor if the cough lasts more than 2 weeks, produces blood or green/yellow mucus, or causes breathing difficulty.",
        "specialist": "Pulmonologist / General Physician",
        "urgency": "ℹ️ Low — home care usually helps; see a doctor if symptoms persist.",
    },
    "headache": {
        "condition": "Headache / Migraine",
        "causes": "Headaches can be caused by dehydration, stress, lack of sleep, migraines, high blood pressure, or sinus issues.",
        "precautions": [
            "Drink adequate water — dehydration is a common trigger.",
            "Rest in a quiet, dark room if light is bothersome.",
            "Apply a cold or warm compress to your forehead.",
            "Avoid screen time and practice deep breathing.",
            "Take OTC pain relievers like ibuprofen or paracetamol.",
        ],
        "see_doctor": "Seek immediate care for sudden severe 'thunderclap' headache, headache with vision loss, confusion, or neck stiffness.",
        "specialist": "Neurologist / General Physician",
        "urgency": "ℹ️ Low — monitor; seek emergency care for sudden severe headache.",
    },
    "cold": {
        "condition": "Common Cold / Upper Respiratory Infection",
        "causes": "The common cold is caused by rhinoviruses and spreads through droplets and contact.",
        "precautions": [
            "Rest and stay warm.",
            "Drink warm fluids — broth, herbal teas, warm water.",
            "Use saline nasal spray to relieve congestion.",
            "Take vitamin C and zinc supplements.",
            "Wash hands frequently to prevent spreading.",
        ],
        "see_doctor": "See a doctor if symptoms worsen after 10 days, or if you develop high fever, ear pain, or shortness of breath.",
        "specialist": "General Physician / ENT Specialist",
        "urgency": "ℹ️ Low — usually resolves in 7–10 days with home care.",
    },
    "sore throat": {
        "condition": "Sore Throat / Pharyngitis",
        "causes": "Sore throat is commonly caused by viral infections (cold, flu), strep bacteria, or allergies.",
        "precautions": [
            "Gargle with warm salt water 3–4 times daily.",
            "Drink warm honey-lemon tea.",
            "Suck on throat lozenges.",
            "Avoid cold foods and drinks.",
            "Stay well-hydrated.",
        ],
        "see_doctor": "See a doctor if throat pain is severe, you have difficulty swallowing, high fever, or swollen lymph nodes in the neck.",
        "specialist": "ENT Specialist / General Physician",
        "urgency": "ℹ️ Low to Moderate — see doctor if swallowing is difficult.",
    },
    "vomiting": {
        "condition": "Nausea / Vomiting / Gastroenteritis",
        "causes": "Vomiting may result from food poisoning, viral gastroenteritis, motion sickness, or overeating.",
        "precautions": [
            "Sip small amounts of water or oral rehydration solution (ORS).",
            "Avoid solid food until vomiting stops.",
            "Try the BRAT diet (Banana, Rice, Applesauce, Toast) once tolerable.",
            "Avoid dairy, fatty, or spicy foods.",
            "Rest and lie down with head elevated.",
        ],
        "see_doctor": "Seek care if vomiting persists more than 24 hours, there is blood in vomit, signs of severe dehydration (dry mouth, no urination), or vomiting with severe abdominal pain.",
        "specialist": "Gastroenterologist / General Physician",
        "urgency": "⚠️ Moderate — see a doctor if it persists or dehydration signs appear.",
    },
    "diarrhea": {
        "condition": "Diarrhea / Gastroenteritis",
        "causes": "Diarrhea is commonly caused by food poisoning, viral or bacterial infections, or lactose intolerance.",
        "precautions": [
            "Drink ORS (Oral Rehydration Solution) to prevent dehydration.",
            "Eat bland foods — rice, banana, boiled potatoes.",
            "Avoid dairy, fatty, and high-fiber foods.",
            "Wash hands thoroughly before meals.",
            "Avoid contaminated water.",
        ],
        "see_doctor": "Seek care if diarrhea contains blood or mucus, lasts more than 2 days, or you develop fever and severe cramps.",
        "specialist": "Gastroenterologist / General Physician",
        "urgency": "⚠️ Moderate — seek urgent care if bloody diarrhea or severe dehydration.",
    },
    "chest pain": {
        "condition": "Chest Pain — Possible Cardiac or Musculoskeletal",
        "causes": "Chest pain can be caused by heart conditions (angina, heart attack), acid reflux, muscle strain, or anxiety.",
        "precautions": [
            "Do NOT ignore chest pain — seek medical attention promptly.",
            "Sit or lie in a comfortable position.",
            "Avoid any physical exertion.",
            "If you have prescribed nitroglycerin, use it.",
            "Call emergency services if pain is crushing, radiates to left arm/jaw, or is accompanied by sweating and breathlessness.",
        ],
        "see_doctor": "🚨 EMERGENCY: If chest pain is severe, crushing, or radiates to the left arm, jaw, or back — call emergency services (108) IMMEDIATELY.",
        "specialist": "Cardiologist / Emergency Medicine",
        "urgency": "🚨 HIGH URGENCY — Seek emergency care immediately.",
    },
    "fatigue": {
        "condition": "Fatigue / Tiredness",
        "causes": "Fatigue can result from poor sleep, anemia, thyroid disorders, diabetes, depression, or overexertion.",
        "precautions": [
            "Ensure 7–9 hours of quality sleep each night.",
            "Maintain a balanced diet rich in iron and vitamins.",
            "Stay hydrated — dehydration worsens fatigue.",
            "Exercise moderately — even a short walk helps.",
            "Reduce stress through meditation or yoga.",
        ],
        "see_doctor": "See a doctor if fatigue is persistent (more than 2 weeks), accompanied by unexplained weight loss, or disrupts daily activities.",
        "specialist": "General Physician / Endocrinologist",
        "urgency": "ℹ️ Low to Moderate — see a doctor if persistent.",
    },
    "dizziness": {
        "condition": "Dizziness / Vertigo",
        "causes": "Dizziness can be caused by dehydration, low blood pressure, inner ear disorders, anemia, or standing up quickly.",
        "precautions": [
            "Sit or lie down immediately when feeling dizzy.",
            "Drink water — dehydration is a common cause.",
            "Avoid sudden position changes (stand up slowly).",
            "Avoid driving or operating machinery.",
            "Eat regular small meals to maintain blood sugar.",
        ],
        "see_doctor": "See a doctor if dizziness is severe, recurrent, or accompanied by hearing loss, ringing in the ear, or fainting.",
        "specialist": "ENT Specialist / Neurologist",
        "urgency": "⚠️ Moderate — seek urgent care if accompanied by fainting.",
    },
    "rash": {
        "condition": "Skin Rash / Allergic Reaction",
        "causes": "Rashes can result from allergies, contact dermatitis, eczema, heat rash, viral infections, or insect bites.",
        "precautions": [
            "Avoid scratching — it worsens irritation and risk of infection.",
            "Apply cool compresses to relieve itching.",
            "Use calamine lotion or hydrocortisone cream.",
            "Identify and avoid potential allergens (food, detergent, fabric).",
            "Wear loose, breathable cotton clothing.",
        ],
        "see_doctor": "See a dermatologist if the rash spreads rapidly, is accompanied by fever, blistering, facial swelling, or difficulty breathing.",
        "specialist": "Dermatologist / Allergist",
        "urgency": "⚠️ Moderate — seek immediate care for rash with breathing difficulty.",
    },
    "stomach pain": {
        "condition": "Abdominal / Stomach Pain",
        "causes": "Stomach pain can be caused by gas, indigestion, gastritis, appendicitis, ulcers, or menstrual cramps.",
        "precautions": [
            "Apply a warm compress to the abdomen.",
            "Avoid spicy, oily, and heavy foods.",
            "Drink peppermint or ginger tea for indigestion.",
            "Eat smaller, frequent meals.",
            "Avoid lying down immediately after eating.",
        ],
        "see_doctor": "Seek emergency care if pain is severe, sudden, or located in the lower right abdomen (appendicitis). Also see a doctor for pain with fever or vomiting.",
        "specialist": "Gastroenterologist / General Physician",
        "urgency": "⚠️ Moderate — emergency care for severe/sudden right-lower pain.",
    },
    "back pain": {
        "condition": "Back Pain / Musculoskeletal",
        "causes": "Back pain commonly results from muscle strain, poor posture, disc problems, kidney issues, or prolonged sitting.",
        "precautions": [
            "Rest, but avoid prolonged bed rest — gentle movement helps.",
            "Apply ice for the first 48 hours, then switch to heat.",
            "Practice good posture while sitting and standing.",
            "Do gentle stretching and core-strengthening exercises.",
            "Use a supportive mattress.",
        ],
        "see_doctor": "See a doctor if pain radiates down the leg (sciatica), is associated with numbness/weakness, or follows an injury.",
        "specialist": "Orthopedic Specialist / Physiotherapist",
        "urgency": "ℹ️ Low to Moderate — see a doctor if persists more than a week.",
    },
    "shortness of breath": {
        "condition": "Breathing Difficulty / Dyspnea",
        "causes": "Shortness of breath can be caused by asthma, COPD, pneumonia, heart conditions, anxiety, or anemia.",
        "precautions": [
            "Sit upright — do NOT lie flat.",
            "Breathe slowly and deeply through pursed lips.",
            "If you have an inhaler, use it immediately.",
            "Move to fresh, cool air.",
            "Do NOT exert yourself — remain calm and still.",
        ],
        "see_doctor": "🚨 URGENT: Severe or sudden shortness of breath is a medical emergency. Call emergency services (108) immediately.",
        "specialist": "Pulmonologist / Cardiologist / Emergency Medicine",
        "urgency": "🚨 HIGH URGENCY — Seek emergency care immediately.",
    },
    "eye pain": {
        "condition": "Eye Pain / Irritation",
        "causes": "Eye pain can be caused by conjunctivitis, eye strain, foreign body, dry eyes, glaucoma, or migraine.",
        "precautions": [
            "Do NOT rub your eyes.",
            "If a foreign body is present, rinse with clean water.",
            "Apply cool compress (not ice directly).",
            "Reduce screen time and take 20-20-20 breaks.",
            "Use artificial tears for dryness.",
        ],
        "see_doctor": "See an eye doctor immediately if pain is severe, accompanied by vision changes, redness, or sensitivity to light.",
        "specialist": "Ophthalmologist",
        "urgency": "⚠️ Moderate — seek urgent care for sudden vision changes.",
    },
}

FALLBACK_RESPONSE = """
I understand you're not feeling well. 🏥

While I couldn't identify a specific match for your symptoms, here are some general tips:

**General Precautions:**
• Stay well-hydrated — drink plenty of water
• Rest adequately and avoid overexertion  
• Monitor your temperature and symptoms
• Avoid self-medicating with antibiotics

**When to See a Doctor:**
• If symptoms persist for more than 2–3 days
• If you experience severe pain, high fever (>103°F), or difficulty breathing
• If you're unsure about your condition

📋 **Try describing your symptoms more specifically**, for example:
*"I have a fever and sore throat"* or *"I have chest pain and shortness of breath"*

⚕️ *Remember: I provide general health information only. Always consult a licensed medical professional for proper diagnosis and treatment.*
"""


def _build_reply(matched_data, user_message):
    """Format a clean, rich reply from matched symptom data."""
    d = matched_data
    precautions_list = "\n".join(f"• {p}" for p in d["precautions"])
    reply = f"""
🩺 **Possible Condition:** {d["condition"]}

📌 **Likely Causes:**
{d["causes"]}

✅ **Precautions & Home Care:**
{precautions_list}

👨‍⚕️ **Doctor's Advice:**
{d["see_doctor"]}

🏥 **Recommended Specialist:** {d["specialist"]}

{d["urgency"]}

---
⚕️ *Disclaimer: This is AI-generated health information for educational purposes only. Always consult a qualified medical professional for diagnosis and treatment.*
"""
    return reply.strip()


def symptom_checker(request):
    """Dedicated full-page symptom checker view."""
    return render(request, 'symptom_checker.html')


@csrf_exempt
def ai_chat(request):
    """AJAX endpoint — receives symptom message, returns AI health advice."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower().strip()
        except (json.JSONDecodeError, AttributeError):
            user_message = request.POST.get('message', '').lower().strip()

        if not user_message:
            return HttpResponse(
                json.dumps({'reply': 'Please describe your symptoms so I can help you.'}),
                content_type='application/json'
            )

        # Match symptoms from knowledge base
        best_match = None
        for keyword, data in SYMPTOM_DB.items():
            if keyword in user_message:
                best_match = data
                break

        if best_match:
            reply = _build_reply(best_match, user_message)
        else:
            reply = FALLBACK_RESPONSE.strip()

        return HttpResponse(
            json.dumps({'reply': reply}),
            content_type='application/json'
        )

    return HttpResponse(
        json.dumps({'error': 'Only POST requests are accepted.'}),
        content_type='application/json',
        status=405
    )

