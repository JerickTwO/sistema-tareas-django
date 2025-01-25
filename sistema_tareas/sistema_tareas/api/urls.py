from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from sistema_tareas.api.views import TareaViewSet

router = DefaultRouter()

router.register('tareas', TareaViewSet, basename='tareas')

urlpatterns = router.urls
