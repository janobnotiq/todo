from django.urls import  path
from django.contrib.auth import views as auth_views

from .views import add_task, delete_task, edit_task, filtered_tasks, home \
    , mark_as_done, mark_as_undone, register,add_comment_view,comments_list_view \
        ,delete_comment,CommentUpdateView

urlpatterns = [
    path("",home,name="home"),
    path("register/",register,name="register"), # type: ignore
    path("accounts/login/",auth_views.LoginView.as_view(template_name="login.html"),name="login"), # type: ignore
    path("logout/",auth_views.LogoutView.as_view(template_name="logout.html"),name="logout"), # type: ignore

    path("add_task/",add_task,name="add-task"), # type: ignore
    path("edit_task/<int:pk>/",edit_task,name="edit-task"), # type: ignore
    path("delete_task/<int:pk>/",delete_task,name="delete-task"), # type: ignore

    path("mark_as_done/<int:pk>/",mark_as_done,name="mark-as-done"),
    path("mark_as_undone/<int:pk>/",mark_as_undone,name="mark-as-undone"),

    path("tasks/<slug:slug>/",filtered_tasks,name="task-by-category"),
    path("add-comment/",add_comment_view,name="add-comment"),
    path("comments/",comments_list_view,name="comments"),
    path("delete-comment/<int:pk>/",delete_comment,name="delete-comment"),
    path("edit-comment/<int:pk>/",CommentUpdateView.as_view(),name="edit-comment"),
]