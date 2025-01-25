from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from tareas.models import Tasks, Comment, User
from sistema_tareas.api.serializer import TasksSerializer


class TasksViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer