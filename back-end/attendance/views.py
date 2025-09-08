from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsTeacherOrAdmin


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing attendance records
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'class_subject', 'date', 'status']
    ordering_fields = ['date', 'student__user__last_name']
    ordering = ['-date']
    
    def get_permissions(self):
        """
        Custom permissions:
        - List/Retrieve/By Student/By Class: Any authenticated user
        - Create/Update/Delete: Teacher or admin only
        """
        if self.action in ['list', 'retrieve', 'by_student', 'by_class']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Only teachers and admins can create/update/delete attendance
            permission_classes = [IsTeacherOrAdmin]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """
        Get attendance records for a specific student
        """
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id is required'}, status=400)
            
        attendance = Attendance.objects.filter(student_id=student_id)
        serializer = self.get_serializer(attendance, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_class(self, request):
        """
        Get attendance records for a specific class
        """
        class_subject_id = request.query_params.get('class_subject_id')
        date = request.query_params.get('date')
        
        if not class_subject_id:
            return Response({'error': 'class_subject_id is required'}, status=400)
            
        queryset = Attendance.objects.filter(class_subject_id=class_subject_id)
        if date:
            queryset = queryset.filter(date=date)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
