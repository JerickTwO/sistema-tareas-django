from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver

User = get_user_model()

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    # Verifica si ya existe un superusuario
    if not User.objects.filter(is_superuser=True).exists():
        # Crea un usuario administrador por defecto
        User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="admin",
            rol=0  # Si tienes un campo `rol` personalizado
        )
        print("Usuario administrador creado: admin")
