from django.urls import path
from service_a import views

urlpatterns = [
    path('', views.tasks, name='tasks'),
    path('<str:task_id>/', views.view_one_task, name='tasks_single'),
    path('api/change-status/', views.change_status, name='change_status'),
]
