from rest_framework import serializers
from .models import Teacher
from users.serializers import UserSerializer

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'user_id', 'employee_id', 'date_of_joining', 'designation',
            'department', 'qualification', 'experience', 'specialization',
            'date_of_birth', 'gender', 'is_active', 'is_class_teacher',
            'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']