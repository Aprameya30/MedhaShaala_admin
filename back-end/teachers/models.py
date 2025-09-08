from django.db import models
from django.conf import settings

class Teacher(models.Model):
    """Teacher model that extends the User model"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    
    # Professional Information
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_joining = models.DateField()
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
    # Qualifications
    qualification = models.CharField(max_length=200, blank=True, null=True)
    experience = models.PositiveIntegerField(default=0, help_text='Experience in years')
    specialization = models.CharField(max_length=200, blank=True, null=True)
    
    # Personal Information
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ))
    
    # Status
    is_active = models.BooleanField(default=True)
    is_class_teacher = models.BooleanField(default=False)
    
    # Additional Information
    remarks = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
    
    class Meta:
        ordering = ['employee_id']
