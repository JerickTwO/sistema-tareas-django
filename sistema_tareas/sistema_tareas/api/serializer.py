from rest_framework import serializers
from tareas.models import Tasks, Comment, User


class TasksSerializer(serializers.ModelSerializer):
    taskStatus = serializers.SerializerMethodField()
    dueDate = serializers.DateTimeField(source="due_date", allow_null=True)
    studentId = serializers.IntegerField(source="user.id")
    studentName = serializers.CharField(source="user.username")

    class Meta:
        model = Tasks
        fields = [
            "id",
            "title",
            "description",
            "dueDate",
            "priority",
            "taskStatus",
            "studentId",
            "studentName",
        ]

    def get_taskStatus(self, obj):
        # Usa el método automático de Django para obtener el texto de STATUS_CHOICES
        return obj.get_task_status_display() or "ESTADO NO DEFINIDO"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="username")
    password = serializers.SerializerMethodField()
    userRole = (
        serializers.SerializerMethodField()
    )  # Mapear 'rol' a 'ADMINISTRADOR' o 'ESTUDIANTE'

    class Meta:
        model = User
        fields = ["id", "name", "email", "password", "userRole"]

    def get_password(self, obj):
        return None  # Ocultar el valor real de la contraseña

    def get_userRole(self, obj):
        return "ADMINISTRADOR" if obj.rol else "ESTUDIANTE"
