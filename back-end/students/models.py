from django.db import models
from django.conf import settings

class Student(models.Model):
    """Student model that extends the User model"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    
    # Academic Information
    admission_number = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_admission = models.DateField()
    
    # Personal Information
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ))
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    
    # Parent/Guardian Information
    parent_name = models.CharField(max_length=100, blank=True, null=True)
    parent_phone = models.CharField(max_length=15, blank=True, null=True)
    parent_email = models.EmailField(blank=True, null=True)
    
    # Academic Status
    is_active = models.BooleanField(default=True)
    current_class = models.ForeignKey('courses.Class', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    current_section = models.CharField(max_length=10, blank=True, null=True)
    
    # Additional Information
    previous_school = models.CharField(max_length=200, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.admission_number} - {self.user.get_full_name()}"
    
    class Meta:
        ordering = ['admission_number']
