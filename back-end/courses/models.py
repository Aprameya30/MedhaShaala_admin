from django.db import models
from django.conf import settings

class AcademicYear(models.Model):
    """Academic Year model"""
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-start_date']

class Class(models.Model):
    """Class model (e.g., Grade 1, Grade 2, etc.)"""
    name = models.CharField(max_length=50)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='classes')
    sections = models.CharField(max_length=100, help_text='Comma-separated list of sections (e.g., A,B,C)')
    class_teacher = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='class_teacher_of')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"
    
    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ['name']
        unique_together = ['name', 'academic_year']

class Subject(models.Model):
    """Subject model"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        ordering = ['name']

class ClassSubject(models.Model):
    """Class-Subject relationship model"""
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classes')
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True, related_name='teaching_subjects')
    
    # Additional fields
    is_optional = models.BooleanField(default=False)
    credits = models.PositiveIntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject.name} for {self.class_obj.name}"
    
    class Meta:
        unique_together = ['class_obj', 'subject']
