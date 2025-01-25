from rest_framework import serializers
from tareas.models import Tasks, Comment, User


# Serializador para tareas
class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "task_status",
            "user",
        ]
        read_only_fields = ["id", "task_status"]

    def validate_due_date(self, value):
        from datetime import datetime

        if value and value < datetime.now():
            raise serializers.ValidationError(
                "La fecha de vencimiento no puede estar en el pasado."
            )
        return value


# Serializador para comentarios
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "create_at", "task", "user"]
        read_only_fields = ["id", "create_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
