from rest_framework import serializers
from .models import ExamType, Exam, Grade
from students.serializers import StudentSerializer
from courses.serializers import ClassSerializer, SubjectSerializer
from users.serializers import UserSerializer

class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExamSerializer(serializers.ModelSerializer):
    exam_type_details = ExamTypeSerializer(source='exam_type', read_only=True)
    class_details = ClassSerializer(source='class_obj', read_only=True)
    subject_details = SubjectSerializer(source='subject', read_only=True)
    
    class Meta:
        model = Exam
        fields = [
            'id', 'name', 'exam_type', 'class_obj', 'subject', 'date',
            'total_marks', 'passing_marks', 'exam_type_details',
            'class_details', 'subject_details', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class GradeSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    exam_details = ExamSerializer(source='exam', read_only=True)
    graded_by_details = UserSerializer(source='graded_by', read_only=True)
    percentage = serializers.ReadOnlyField()
    is_pass = serializers.ReadOnlyField()
    
    class Meta:
        model = Grade
        fields = [
            'id', 'student', 'exam', 'marks_obtained', 'remarks',
            'graded_by', 'student_details', 'exam_details',
            'graded_by_details', 'percentage', 'is_pass',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'percentage', 'is_pass']