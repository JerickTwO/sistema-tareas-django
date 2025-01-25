from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
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


class Tarea(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
    )

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    asignada_a = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='tareas',
        limit_choices_to={'rol': 'estudiante'}
    )
    creada_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='tareas_creadas',
        limit_choices_to={'rol': 'admin'}
    )
    estado = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')
    comentado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'estudiante'}
    )
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.comentado_por.username} en {self.tarea.titulo}"
