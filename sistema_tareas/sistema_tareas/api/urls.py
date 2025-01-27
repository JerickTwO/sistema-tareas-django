from django.urls import path
from sistema_tareas.api.views import (
    UserListView,
    TasksCreateView,
    TasksUpdateView,
    TasksListView,
    TasksDeleteView,
    TasksDetailView,
    create_comment,
    get_comments_by_tasks,
    search_tasks,
    StudentTasksController,
    UpdateTaskStatusController,
    GetTaskByIdController,
    CreateCommentController,
    GetCommentsByTaskController,
)

urlpatterns = [
 # Rutas de AdminController
    path("admin/users", UserListView.as_view(), name="get_users"),
    path("admin/task", TasksCreateView.as_view(), name="post_task"),
    path("admin/task/<int:id>", TasksUpdateView.as_view(), name="task_detail_update"),
    path("admin/tasks/search/<str:title>", search_tasks, name="search_task"),
    path("admin/tasks", TasksListView.as_view(), name="get_all_tasks"),
    path("admin/task/delete/<int:id>", TasksDeleteView.as_view(), name="delete_task"),
    path("admin/task/comment/<int:id>", create_comment, name="create_comment"),
    path("admin/comments/<int:id>", get_comments_by_tasks, name="get_comments_by_task"),
    
    # Rutas de UserController
    path("student/tasks", StudentTasksController.as_view(), name="get_student_tasks"),
    path("student/task/<int:id>/<str:status>", UpdateTaskStatusController.as_view(), name="update_task_status"),
    path("student/task/<int:id>", GetTaskByIdController.as_view(), name="get_task_by_id"),
    path("student/task/comment/<int:task_id>", CreateCommentController.as_view(), name="create_comment"),
    path("student/comments/<int:task_id>", GetCommentsByTaskController.as_view(), name="get_comments_by_task"),

]
