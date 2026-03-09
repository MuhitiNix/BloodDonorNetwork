from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta

def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("You must be at least 18 years old to donate blood.")

class DonorProfile(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')
    ])

    date_of_birth = models.DateField(validators=[validate_age])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    occupation = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15)
    
    
    last_donation_date = models.DateField(null=True, blank=True)
    total_donations = models.PositiveIntegerField(default=0)
    
    location = models.PointField(srid=4326, null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def clean(self):
        
        if self.last_donation_date:
            four_months_ago = date.today() - timedelta(days=120)
            if self.last_donation_date > four_months_ago:
                self.is_available = False 
        super().clean()

    def __str__(self):
        return f"{self.user.username} ({self.blood_group})"

