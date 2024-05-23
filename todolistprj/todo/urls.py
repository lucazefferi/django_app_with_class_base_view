from django.urls import path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, CustomRegisterView
from django.contrib.auth.views import LogoutView

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    #path('tasklist/', views.task_list, name='task_list'), se avessimo usato (def task_list)
    path('tasklist/', TaskList.as_view(), name='task_list'),
    #path('taskdetail/<int:task_id>', views.task_detail, name='task_detail') se avessimo usato (def task_detail)
    path('taskdetail/<int:pk>', TaskDetail.as_view(), name='task_detail'),
    path('taskcreate/', TaskCreate.as_view(), name='task_create'),
    path('taskupdate/<int:pk>', TaskUpdate.as_view(), name='task_update'),
    #path('task/delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('taskdelete/<int:pk>', TaskDelete.as_view(), name='task_delete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page="todo:login"), name='logout') #next_page="todo:login" è dove ci rimanda qundo facciamo logout, altrimenti ci manderebbe alla pagina di default logout di djnago
]



