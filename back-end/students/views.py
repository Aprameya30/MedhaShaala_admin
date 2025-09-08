from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Student
from .serializers import StudentSerializer
from users.models import User
from users.permissions import IsOwnerOrAdmin, IsTeacherOrAdmin


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing students
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_permissions(self):
        """
        Custom permissions:
        - List/Retrieve/Active: Any authenticated user
        - Update/Delete: Owner or admin only
        - Create: Admin or teacher only
        """
        if self.action in ['list', 'retrieve', 'active']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'create':
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Handle nested user creation
        user_data = self.request.data.get('user', {})
        if user_data:
            with transaction.atomic():
                # Create user first
                user = User.objects.create_user(
                    email=user_data.get('email'),
                    first_name=user_data.get('first_name', ''),
                    last_name=user_data.get('last_name', ''),
                    phone_number=user_data.get('phone_number', ''),
                    address=user_data.get('address', ''),
                    user_type='student'
                )
                serializer.save(user=user)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get all active students
        """
        active_students = Student.objects.filter(is_active=True)
        serializer = self.get_serializer(active_students, many=True)
        return Response(serializer.data)
