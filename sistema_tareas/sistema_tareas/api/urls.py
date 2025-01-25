from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from sistema_tareas.api.views import TasksViewSet

router = DefaultRouter()

router.register('tasks', TasksViewSet, basename='tareas')

urlpatterns = router.urls
