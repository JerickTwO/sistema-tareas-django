from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('estudiante', 'Estudiante'),
    )
    rol = models.CharField(max_length=10, choices=ROLES)

    # Solución al problema de las relaciones reversas
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_groups',  # Cambiar el related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions',  # Cambiar el related_name
        blank=True
    )

    def __str__(self):
        return self.username


class Tasks(models.Model):
    title = models.CharField(max_length=255)               # Título de la tarea
    description = models.TextField(null=True, blank=True)  # Descripción (opcional)
    due_date = models.DateTimeField(null=True, blank=True) # Fecha de vencimiento (opcional)
    priority = models.CharField(max_length=255, null=True, blank=True)  # Prioridad
    task_status = models.BooleanField(default=False)       # Estado de la tarea (False = pendiente, True = completada)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario (clave foránea)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()                           # Contenido del comentario
    create_at = models.DateTimeField(auto_now_add=True)    # Fecha de creación (se genera automáticamente)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='comments')  # Relación con la tarea
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario

    def __str__(self):
        return f"Comentario de {self.user.username} en {self.task.title}"