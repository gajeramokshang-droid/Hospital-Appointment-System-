from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

from .models import Doctor, Patient, Appointment
from .forms import SignupForm, AppointmentForm


def home(request):
    return redirect('doctor_list')


# ─── Auth ────────────────────────────────────────────────────────────────────

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('doctor_list')

    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        Patient.objects.create(
            user=user,
            age=form.cleaned_data['age'],
            contact=form.cleaned_data['contact'],
        )

        login(request, user)
        messages.success(request, 'Account created! Welcome.')
        return redirect('doctor_list')

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('doctor_list')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'doctor_list'))
        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Doctors ─────────────────────────────────────────────────────────────────

def doctor_list(request):
    doctors = Doctor.objects.all()

    query = request.GET.get('q', '').strip()
    department = request.GET.get('department', '').strip()

    if query:
        doctors = doctors.filter(name__icontains=query)

    if department:
        doctors = doctors.filter(department__iexact=department)

    departments = Doctor.objects.values_list('department', flat=True).distinct().order_by('department')

    return render(request, 'doctors.html', {
        'doctors': doctors,
        'departments': departments,
        'query': query,
        'selected_department': department,
    })


# ─── Appointments ─────────────────────────────────────────────────────────────

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)

    # Ensure the logged-in user has a Patient profile
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, 'No patient profile found for your account.')
        return redirect('doctor_list')

    form = AppointmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False)
        appointment.doctor = doctor
        appointment.patient = patient
        appointment.status = 'Scheduled'

        try:
            appointment.save()
            messages.success(request, f'Appointment booked with {doctor} on {appointment.date_time}.')
            return redirect('appointment_history')
        except IntegrityError:
            messages.error(request, 'You already have an appointment with this doctor at that date/time.')

    return render(request, 'book.html', {'form': form, 'doctor': doctor})


@login_required
def appointment_history(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, 'No patient profile found.')
        return redirect('doctor_list')

    appointments = Appointment.objects.filter(patient=patient).select_related('doctor').order_by('-date_time')
    return render(request, 'appointments.html', {'appointments': appointments})


@login_required
def cancel_appointment(request, appointment_id):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, 'No patient profile found.')
        return redirect('doctor_list')

    appointment = get_object_or_404(Appointment, pk=appointment_id)

    # Only the booking patient can cancel
    if appointment.patient != patient:
        messages.error(request, 'You can only cancel your own appointments.')
        return redirect('appointment_history')

    if appointment.status == 'Cancelled':
        messages.info(request, 'This appointment is already cancelled.')
        return redirect('appointment_history')

    if request.method == 'POST':
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled.')
        return redirect('appointment_history')

    return render(request, 'cancel_confirm.html', {'appointment': appointment})
