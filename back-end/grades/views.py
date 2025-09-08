from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import ExamType, Exam, Grade
from .serializers import ExamTypeSerializer, ExamSerializer, GradeSerializer
from users.permissions import IsTeacherOrAdmin


class ExamTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing exam types
    """
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer
    
    def get_permissions(self):
        """
        Custom permissions:
        - List/Retrieve: Any authenticated user
        - Create/Update/Delete: Teacher or admin only
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsTeacherOrAdmin]
        return [permission() for permission in permission_classes]


class ExamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing exams
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['exam_type', 'class_obj', 'subject', 'date']
    ordering_fields = ['date', 'name']
    ordering = ['-date']
    
    def get_permissions(self):
        """
        Custom permissions:
        - List/Retrieve/Grades: Any authenticated user
        - Create/Update/Delete: Teacher or admin only
        """
        if self.action in ['list', 'retrieve', 'grades']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsTeacherOrAdmin]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def grades(self, request, pk=None):
        """
        Get all grades for a specific exam
        """
        exam = self.get_object()
        grades = Grade.objects.filter(exam=exam)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)


class GradeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing grades
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'exam', 'exam__exam_type']
    ordering_fields = ['exam__date', 'marks_obtained']
    ordering = ['-exam__date']
    
    def get_permissions(self):
        """
        Custom permissions:
        - List/Retrieve/By Student/By Class: Any authenticated user
        - Create/Update/Delete: Teacher or admin only
        """
        if self.action in ['list', 'retrieve', 'by_student', 'by_class']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Only teachers and admins can create/update/delete grades
            permission_classes = [IsTeacherOrAdmin]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(graded_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """
        Get grades for a specific student
        """
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id is required'}, status=400)
            
        grades = Grade.objects.filter(student_id=student_id)
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_class(self, request):
        """
        Get grades for a specific class and exam
        """
        class_id = request.query_params.get('class_id')
        exam_id = request.query_params.get('exam_id')
        
        if not class_id or not exam_id:
            return Response({'error': 'class_id and exam_id are required'}, status=400)
            
        grades = Grade.objects.filter(exam__class_obj_id=class_id, exam_id=exam_id)
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)
