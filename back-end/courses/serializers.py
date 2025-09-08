from rest_framework import serializers
from .models import AcademicYear, Class, Subject, ClassSubject
from teachers.serializers import TeacherSerializer

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClassSerializer(serializers.ModelSerializer):
    class_teacher = TeacherSerializer(read_only=True)
    class_teacher_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Class
        fields = ['id', 'name', 'academic_year', 'sections', 'class_teacher', 'class_teacher_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClassSubjectSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    teacher_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    subject_details = SubjectSerializer(source='subject', read_only=True)
    class_details = ClassSerializer(source='class_obj', read_only=True)
    
    class Meta:
        model = ClassSubject
        fields = ['id', 'class_obj', 'subject', 'teacher', 'teacher_id', 'is_optional', 'credits', 'subject_details', 'class_details', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']