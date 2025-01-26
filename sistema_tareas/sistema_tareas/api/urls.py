from django.urls import path
from sistema_tareas.api.views import AdminController, StudentController

urlpatterns = [
    # Rutas de AdminController
    path("admin/users", AdminController.as_view(), name="get_users"),
    path("admin/task", AdminController.as_view(), name="create_task"),
    path("admin/tasks", AdminController.as_view(), name="get_all_tasks"),
    path("admin/task/<int:id>", AdminController.as_view(), name="delete_task"),
    path("admin/task/<int:id>", AdminController.as_view(), name="update_task"),
    path(
        "admin/tasks/search/<str:title>", AdminController.as_view(), name="search_task"
    ),
    path(
        "admin/task/comment/<int:task_id>",
        AdminController.as_view(),
        name="post_comment",
    ),
    path(
        "admin/comments/<int:task_id>",
        AdminController.as_view(),
        name="get_comments_by_task",
    ),
    # Rutas de StudentController
    path("student/tasks", StudentController.as_view(), name="get"),
    path(
        "student/task/<int:id>/<str:status>",
        StudentController.as_view(),
        name="update_task",
    ),
    path("student/task/<int:id>", StudentController.as_view(), name="get_task_by_id"),
    path(
        "student/task/comment/<int:task_id>",
        StudentController.as_view(),
        name="post_comment",
    ),
    path(
        "student/comments/<int:task_id>",
        StudentController.as_view(),
        name="get_comments_by_task",
    ),
]
