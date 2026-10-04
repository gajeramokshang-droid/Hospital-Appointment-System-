from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)

    def __str__(self):
        return f"Dr. {self.name} ({self.department})"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Cancelled', 'Cancelled'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    class Meta:
        unique_together = ('doctor', 'patient', 'date_time')

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.date_time} [{self.status}]"
