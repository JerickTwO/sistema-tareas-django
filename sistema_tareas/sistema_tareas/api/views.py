from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tareas.models import User, Tasks, Comment
from sistema_tareas.api.serializer import (
    UserSerializer,
    TasksSerializer,
    CommentSerializer,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# GET all users
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# POST a new tasks
class TasksCreateView(APIView):
    permission_classes = [IsAuthenticated]

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


# PUT update a tasks
class TasksUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            tasks = Tasks.objects.get(id=id)
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TasksSerializer(tasks, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET para obtener una tarea por ID
    def get(self, request, id):
        try:
            tasks = Tasks.objects.get(id=id)
            serializer = TasksSerializer(tasks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND
            )

    # PUT para actualizar una tarea por ID
    def put(self, request, id):
        try:
            tasks = Tasks.objects.get(id=id)
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TasksSerializer(tasks, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Eliminar una tarea por ID
    def delete(self, request, id):
        try:
            task = Tasks.objects.get(id=id)
            task.delete()
            return Response(
                {"message": "Task deleted successfully"}, status=status.HTTP_200_OK
            )
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )


# GET search tasks by title
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_tasks(request, title):
    taskss = Tasks.objects.filter(title__icontains=title)
    serializer = TasksSerializer(taskss, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# GET all taskss
class TasksListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        taskss = Tasks.objects.all()
        serializer = TasksSerializer(taskss, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# DELETE a tasks
class TasksDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            tasks = Tasks.objects.get(id=id)
            tasks.delete()
            return Response(
                {"message": "Tasks deleted successfully"}, status=status.HTTP_200_OK
            )
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND
            )


# GET tasks by ID
class TasksDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            tasks = Tasks.objects.get(id=id)
            serializer = TasksSerializer(tasks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response(
                {"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND
            )


# POST create a comment
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request, id):
    try:
        tasks = Tasks.objects.get(id=id)
    except Tasks.DoesNotExist:
        return Response({"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND)

    content = request.data.get("content", "")
    if not content:
        return Response(
            {"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    comment = Comment.objects.create(tasks=tasks, content=content)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# GET comments by tasks
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_comments_by_tasks(request, id):
    comments = Comment.objects.filter(tasks_id=id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
