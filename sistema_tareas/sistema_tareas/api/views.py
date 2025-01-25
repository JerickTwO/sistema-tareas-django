from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from tareas.models import Tarea, Comentario, Usuario
from sistema_tareas.api.serializer import TareaSerializer


class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer