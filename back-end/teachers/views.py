from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Teacher
from .serializers import TeacherSerializer
from users.models import User
from users.permissions import IsOwnerOrAdmin


class TeacherViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing teachers
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    
    def get_permissions(self):
        """
        Custom permissions:
        - List/Retrieve/Active: Any authenticated user
        - Update/Delete: Owner or admin only
        - Create: Admin only
        """
        if self.action in ['list', 'retrieve', 'active']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
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
                    user_type='teacher'
                )
                serializer.save(user=user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        # Handle nested user update
        user_data = self.request.data.get('user', {})
        if user_data and serializer.instance.user:
            with transaction.atomic():
                user = serializer.instance.user
                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)
                user.email = user_data.get('email', user.email)
                user.phone_number = user_data.get('phone_number', user.phone_number)
                user.address = user_data.get('address', user.address)
                user.save()
                serializer.save()
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get all active teachers
        """
        active_teachers = Teacher.objects.filter(is_active=True)
        serializer = self.get_serializer(active_teachers, many=True)
        return Response(serializer.data)
