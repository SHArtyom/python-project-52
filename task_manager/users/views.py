from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthRequiredMixin, UserPermissionMixin,\
    DeleteProtectionMixin
from .models import User
from .forms import UserForm


class UsersListView(ListView):

    template_name = 'users/users.html'
    model = User
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):

    template_name = 'users/form_create.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = _('User is successfully registered')


class UserUpdateView(AuthRequiredMixin, UserPermissionMixin,
                     SuccessMessageMixin, UpdateView):

    template_name = 'users/form_update.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users')
    success_message = _('User is successfully updated')
    permission_message = _('You have no rights to change another user.')
    permission_url = reverse_lazy('users')


class UserDeleteView(AuthRequiredMixin, UserPermissionMixin,
                     DeleteProtectionMixin, SuccessMessageMixin, DeleteView):

    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('users')
    success_message = _('User is successfully deleted')
    permission_message = _('You have no rights to change another user.')
    permission_url = reverse_lazy('users')
    protected_message = _('Unable to delete a user because he is being used')
    protected_url = reverse_lazy('users')
