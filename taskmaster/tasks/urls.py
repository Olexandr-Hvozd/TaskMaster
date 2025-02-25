from django.urls import path

from . import views

urlpatterns = [
    path("", views.TaskHome.as_view(), name='home'),
    path("add_task/", views.AddTask.as_view(), name='add_task'),
    path('task/delete/<int:task_id>/', views.DeleteTask.as_view(), name='delete_task'),
    path('task/edit/<int:task_id>/', views.EditTask.as_view(), name='edit_task'),
    path('task/done/<int:task_id>/', views.DoneTask.as_view(), name='to_done_task'),
    path('task/details/<int:task_id>/', views.TaskDetail.as_view(), name='task_details'),
    path('task/active_task/<int:task_id>/', views.ActiveTask.as_view(), name='to_active_task'),
]



