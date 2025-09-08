from rest_framework import serializers
from .models import Attendance
from students.serializers import StudentSerializer
from courses.serializers import ClassSubjectSerializer
from users.serializers import UserSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    class_subject_details = ClassSubjectSerializer(source='class_subject', read_only=True)
    marked_by_details = UserSerializer(source='marked_by', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'class_subject', 'date', 'status', 'remarks',
            'marked_by', 'student_details', 'class_subject_details',
            'marked_by_details', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']