from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from sistema_tareas.api.views import TasksViewSet, CommentViewSet

router = DefaultRouter()

router.register('tasks', TasksViewSet, basename='tareas')
router.register('comments', CommentViewSet, basename='comentarios')


urlpatterns = router.urls
