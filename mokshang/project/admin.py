from django.contrib import admin
from .models import Doctor, Patient, Appointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'specialization')
    search_fields = ('name', 'department', 'specialization')
    list_filter = ('department',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'contact')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_time', 'status')
    list_filter = ('status', 'doctor__department')
    search_fields = ('patient__user__username', 'doctor__name')
    list_editable = ('status',)
