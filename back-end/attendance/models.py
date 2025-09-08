from django.db import models
from django.conf import settings

class Attendance(models.Model):
    """Attendance model for tracking student attendance"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='attendances')
    class_subject = models.ForeignKey('courses.ClassSubject', on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    date = models.DateField()
    
    # Attendance status choices
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    
    # Additional information
    remarks = models.TextField(blank=True, null=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='marked_attendances')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"
    
    class Meta:
        unique_together = ['student', 'class_subject', 'date']
        ordering = ['-date', 'student__admission_number']
