from django.contrib import admin
from django.urls import path, include
from task_manager.views import IndexView, UserLoginView, UserLogoutView


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls, name='admin'),
    path('users/', include('task_manager.users.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
]
