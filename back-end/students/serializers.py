from rest_framework import serializers
from .models import Student
from users.serializers import UserSerializer

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'user_id', 'admission_number', 'roll_number', 'date_of_admission',
            'date_of_birth', 'gender', 'blood_group', 'parent_name', 'parent_phone',
            'parent_email', 'is_active', 'current_class', 'current_section',
            'previous_school', 'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']