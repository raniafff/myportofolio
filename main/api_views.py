from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Project, Education
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import ProjectSerializer, EducationSerializer


# ==============================================================================
# PROJECT API VIEWS
# ==============================================================================

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def api_project_list(request):
    """
    List all projects (with optional search query 'q' or 'title') or create a new project.
    - GET: Public (Visitor, Regular User, Editor, Owner)
    - POST: Restricted to Owner (Superuser)
    """
    if request.method == 'GET':
        query = (request.GET.get('q', '') or request.GET.get('title', '')).strip()
        projects = Project.objects.all().order_by('-id')
        if query:
            projects = projects.filter(
                Q(title__icontains=query) |
                Q(tech_stack__icontains=query) |
                Q(description__icontains=query)
            )
        serializer = ProjectSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def api_project_detail(request, id):
    """
    Retrieve, update or delete a specific project by UUID.
    - GET: Public
    - PUT / PATCH: Owner and Editor
    - DELETE: Restricted to Owner (Superuser)
    """
    project = get_object_or_404(Project, pk=id)

    if request.method == 'GET':
        serializer = ProjectSerializer(project, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ['PUT', 'PATCH']:
        partial = (request.method == 'PATCH')
        serializer = ProjectSerializer(
            project,
            data=request.data,
            partial=partial,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_project_toggle_star(request, id):
    """
    Toggle star status of a project for the authenticated user.
    Available to any authenticated user (Regular User, Editor, Owner).
    """
    project = get_object_or_404(Project, pk=id)
    if request.user in project.starred_by.all():
        project.starred_by.remove(request.user)
        is_starred = False
    else:
        project.starred_by.add(request.user)
        is_starred = True

    return Response({
        "status": "success",
        "is_starred": is_starred,
        "star_count": project.starred_by.count()
    }, status=status.HTTP_200_OK)


# ==============================================================================
# EDUCATION API VIEWS
# ==============================================================================

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def api_education_list(request):
    """
    List all education entries (with optional search query 'q') or create a new entry.
    - GET: Public
    - POST: Restricted to Owner (Superuser)
    """
    if request.method == 'GET':
        query = (request.GET.get('q', '') or request.GET.get('institution', '')).strip()
        educations = Education.objects.all().order_by('-start_year')
        if query:
            educations = educations.filter(
                Q(institution__icontains=query) |
                Q(degree__icontains=query) |
                Q(description__icontains=query)
            )
        serializer = EducationSerializer(educations, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = EducationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def api_education_detail(request, id):
    """
    Retrieve, update or delete a specific education entry by Integer ID.
    - GET: Public
    - PUT / PATCH: Owner and Editor
    - DELETE: Restricted to Owner (Superuser)
    """
    education = get_object_or_404(Education, pk=id)

    if request.method == 'GET':
        serializer = EducationSerializer(education, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ['PUT', 'PATCH']:
        partial = (request.method == 'PATCH')
        serializer = EducationSerializer(
            education,
            data=request.data,
            partial=partial,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_education_toggle_star(request, id):
    """
    Toggle star status of an education entry for the authenticated user.
    """
    education = get_object_or_404(Education, pk=id)
    if request.user in education.starred_by.all():
        education.starred_by.remove(request.user)
        is_starred = False
    else:
        education.starred_by.add(request.user)
        is_starred = True

    return Response({
        "status": "success",
        "is_starred": is_starred,
        "star_count": education.starred_by.count()
    }, status=status.HTTP_200_OK)

