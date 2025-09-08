from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AcademicYear, Class, Subject, ClassSubject
from .serializers import AcademicYearSerializer, ClassSerializer, SubjectSerializer, ClassSubjectSerializer


class AcademicYearViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing academic years
    """
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing classes
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        """
        Get all subjects for a specific class
        """
        class_obj = self.get_object()
        class_subjects = ClassSubject.objects.filter(class_obj=class_obj)
        serializer = ClassSubjectSerializer(class_subjects, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing subjects
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class ClassSubjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing class subjects
    """
    queryset = ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class SectionListView(APIView):
    """
    API endpoint for getting all sections from classes
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get all unique sections from all classes
        classes = Class.objects.all()
        sections = set()
        
        for class_obj in classes:
            if class_obj.sections:
                class_sections = [s.strip() for s in class_obj.sections.split(',')]
                sections.update(class_sections)
        
        # Convert to list of dictionaries for consistent API response
        section_list = [{'id': i+1, 'name': section} for i, section in enumerate(sorted(sections))]
        
        return Response({
            'count': len(section_list),
            'next': None,
            'previous': None,
            'results': section_list
        })
