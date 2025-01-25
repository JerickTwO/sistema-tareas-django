from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from tareas.models import Tasks, Comment, User
from sistema_tareas.api.serializer import TasksSerializer,CommentSerializer


# Vista para las tareas
class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Asignar automáticamente el usuario autenticado a la tarea
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Filtrar las tareas por el usuario autenticado
        return Tasks.objects.filter(user=self.request.user)


# Vista para los comentarios
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Asignar automáticamente el usuario autenticado al comentario
        serializer.save(user=self.request.user)
