from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tareas.models import User, Tasks, Comment
from sistema_tareas.api.serializer import (
    UserSerializer,
    TasksSerializer,
    CommentSerializer,
)
from rest_framework.permissions import IsAuthenticated


class AdminController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if "tasks" in request.path:
            return self.get_all_tasks(request)
        elif "users" in request.path:
            return self.get_all_users(request)
        return Response(
            {"error": "Invalid endpoint"}, status=status.HTTP_400_BAD_REQUEST
        )

    def get_all_users(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_all_tasks(self, request):
        tasks = Tasks.objects.all()
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Crear una tarea
    def post(self, request):
        serializer = TasksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                (serializer.data),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # Eliminar una tarea
    def delete_task(self, request, id):
        try:
            task = Tasks.objects.get(pk=id)
            task.delete()
            return Response(
                {"message": "Task deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # Obtener una tarea por ID
    def get_task(self, request, id):
        try:
            task = Tasks.objects.get(pk=id)
            serializer = TasksSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # Actualizar una tarea
    def put(self, request, id):
        try:
            task = Tasks.objects.get(pk=id)
            serializer = TasksSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Task updated successfully", "task": serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # Buscar tarea por título
    def search_task(self, request, title):
        tasks = Tasks.objects.filter(title__icontains=title)
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Crear un comentario
    def post_comment(self, request, task_id):
        content = request.data.get("content")
        if not content:
            return Response(
                {"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            task = Tasks.objects.get(pk=task_id)
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

        comment = Comment.objects.create(task=task, user=request.user, content=content)
        serializer = CommentSerializer(comment)
        return Response(
            {"message": "Comment created successfully", "comment": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    # Obtener comentarios de una tarea
    def get_comments_by_task(self, request, task_id):
        comments = Comment.objects.filter(task_id=task_id)
        serializer = CommentSerializer(comments, many=True)
        return Response({"comments": serializer.data}, status=status.HTTP_200_OK)


class StudentController(APIView):
    permission_classes = [IsAuthenticated]

    # Obtener tareas del usuario autenticado
    def get(self, request):
        tasks = Tasks.objects.filter(user=request.user)
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Actualizar el estado de una tarea
    def patch(self, request, id, status):
        try:
            task = Tasks.objects.get(pk=id, user=request.user)
            task.task_status = status.lower() == "completed"
            task.save()
            serializer = TasksSerializer(task)
            return Response(
                {"message": "Task updated successfully", "task": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # Obtener una tarea por ID
    def get_task_by_id(self, request, id):
        try:
            task = Tasks.objects.get(pk=id, user=request.user)
            serializer = TasksSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # Crear un comentario
    def post_comment(self, request, task_id):
        content = request.data.get("content")
        if not content:
            return Response(
                {"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            task = Tasks.objects.get(pk=task_id, user=request.user)
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

        comment = Comment.objects.create(task=task, user=request.user, content=content)
        serializer = CommentSerializer(comment)
        return Response(
            {"message": "Comment created successfully", "comment": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    # Obtener comentarios por tarea
    def get_comments_by_task(self, request, task_id):
        comments = Comment.objects.filter(task_id=task_id, task__user=request.user)
        serializer = CommentSerializer(comments, many=True)
        return Response({"comments": serializer.data}, status=status.HTTP_200_OK)
