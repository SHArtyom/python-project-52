from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.test import TestCase, Client
from task_manager.users.models import User
from django.core.exceptions import ObjectDoesNotExist
import os
import json


def load_data(path):
    with open(os.path.abspath(f'task_manager/fixtures/{path}'), 'r') as file:
        return json.loads(file.read())


class UserTestCase(TestCase):
    fixtures = ['base_users.json']
    test_user = load_data('test_users.json')

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.users = User.objects.all()
        self.count = User.objects.count()


class TestCreateUser(UserTestCase):
    def test_create_valid_user(self):
        user_data = self.test_user['create_test']['valid_user'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(User.objects.last().username, user_data['username'])

    def test_create_fields_missing(self):
        user_data = self.test_user['create_test']['missing_fields_user'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors
        error_help = _('This field is required.')
        self.assertIn('username', errors)
        self.assertEqual([error_help], errors['username'])
        self.assertIn('first_name', errors)
        self.assertEqual([error_help], errors['first_name'])
        self.assertIn('last_name', errors)
        self.assertEqual([error_help], errors['last_name'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_invalid_username(self):
        user_data = self.test_user['create_test']['invalid_username'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors
        self.assertIn('username', errors)
        self.assertEqual(
            [_('Enter a valid username. This value may contain only '
               'letters, numbers, and @/./+/-/_ characters.')],
            errors['username'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_username_exists(self):
        user_data = self.test_user['create_test']['existing_user'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors
        self.assertIn('username', errors)
        self.assertEqual(
            [_('A user with that username already exists.')],
            errors['username'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_long_fields(self):
        user_data = self.test_user['create_test']['valid_user'].copy()
        user_data.update({'username': 'username' * 20})
        user_data.update({'first_name': 'firstname' * 20})
        user_data.update({'last_name': 'lastname' * 20})
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors
        self.assertIn('username', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters (it has 160).')],
            errors['username'])
        self.assertIn('first_name', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters (it has 180).')],
            errors['first_name'])
        self.assertIn('last_name', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters (it has 160).')],
            errors['last_name'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_missing(self):
        user_data = self.test_user['create_test']['no_password_user'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors
        error_help = _('This field is required.')
        self.assertIn('password1', errors)
        self.assertEqual([error_help], errors['password1'])
        self.assertIn('password2', errors)
        self.assertEqual([error_help], errors['password2'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_dont_match(self):
        user_data = self.test_user['create_test']['typo_password_user'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors
        self.assertIn('password2', errors)
        self.assertEqual(
            [_('The two password fields didn’t match.')],
            errors['password2'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_too_short(self):
        user_data = self.test_user['create_test']['short_password_user'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors
        self.assertIn('password2', errors)
        self.assertEqual(
            [_('This password is too short. '
               'It must contain at least 3 characters.')],
            errors['password2'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)


class TestUpdateUser(UserTestCase):
    def test_update_self(self):
        self.client.force_login(self.user2)
        user_data = self.test_user['update_user'].copy()
        response = self.client.post(
            reverse_lazy('user_update', kwargs={'pk': 2}), data=user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertEqual(User.objects.count(), self.count)
        self.assertEqual(User.objects.get(id=self.user2.id).first_name,
                         user_data['first_name'])

    def test_update_other(self):
        self.client.force_login(self.user1)
        user_data = self.test_user['update_user'].copy()
        response = self.client.post(
            reverse_lazy('user_update', kwargs={'pk': 2}), data=user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertEqual(User.objects.count(), self.count)
        self.assertNotEqual(
            User.objects.get(id=self.user2.id).first_name,
            user_data['first_name'])


class TestDeleteUser(UserTestCase):
    def test_delete_self(self):
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse_lazy('user_delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertEqual(User.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=self.user2.id)

    def test_delete_other(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse_lazy('user_delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertEqual(User.objects.count(), self.count)
