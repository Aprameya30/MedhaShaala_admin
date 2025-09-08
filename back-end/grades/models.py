from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class ExamType(models.Model):
    """Exam Type model (e.g., Mid-term, Final, Quiz, etc.)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Exam(models.Model):
    """Exam model"""
    name = models.CharField(max_length=100)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='exams')
    class_obj = models.ForeignKey('courses.Class', on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey('courses.Subject', on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    total_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=35)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject.name} ({self.class_obj.name})"
    
    class Meta:
        ordering = ['-date']

class Grade(models.Model):
    """Grade model for tracking student grades"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='grades')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grades')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Additional fields
    remarks = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='graded_exams')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student} - {self.exam} - {self.marks_obtained}"
    
    class Meta:
        unique_together = ['student', 'exam']
        ordering = ['-exam__date', 'student__admission_number']
    
    @property
    def percentage(self):
        """Calculate percentage of marks obtained"""
        return (self.marks_obtained / self.exam.total_marks) * 100
    
    @property
    def is_pass(self):
        """Check if student passed the exam"""
        return self.marks_obtained >= self.exam.passing_marks
