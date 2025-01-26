from rest_framework import serializers
from tareas.models import Tasks, Comment, User


class TasksSerializer(serializers.ModelSerializer):
    studentId = serializers.SerializerMethodField()
    studentName = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "task_status",
            "studentId",
            "studentName",
        ]

    def get_studentId(self, obj):
        return obj.user.id if obj.user else None

    def get_studentName(self, obj):
        return obj.user.username if obj.user else None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="username")  # Renombrar 'username' a 'name'
    password = serializers.SerializerMethodField()  # Siempre devolver 'null'
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
