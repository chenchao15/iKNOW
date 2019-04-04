from backend.models import *
from userpage.views import *
import json
import time

from rest_framework import status
from rest_framework.test import APITestCase

userpage_url = '/api/userpage/'


class SignUpTests(APITestCase):

    url = userpage_url + 'signup'

    def test_post_success_contestant(self):
        data = {'username': 'test_username', 'email':'test_email@test.com', 'password': 'test_password', 'usertype': '0'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username=data['username']).email, data['email'])
        self.assertEqual(User.objects.get(username=data['username']).id, response.data.get('id'))
        self.assertEqual(User.objects.get(username=data['username']).first_name, 'contestant')

    def test_post_success_organizer(self):
        data = {'username': 'test_username', 'email':'test_email@test.com', 'password':'test_password', 'usertype':'1'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username=data['username']).email, data['email'])
        self.assertEqual(User.objects.get(username=data['username']).id, response.data.get('id'))
        self.assertEqual(User.objects.get(username=data['username']).first_name, 'organizer')

    def test_post_wrong_usertype(self):
        data = {'username': 'test_username', 'email':'test_email@test.com', 'password':'test_password', 'usertype':'2'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('signup'), 1)
        self.assertEqual(User.objects.count(), 0)

    def test_post_bad_email_format(self):
        data = {'username': 'test_username', 'email':'bad_mail', 'password':'test_password', 'usertype': 0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('signup'), 1)
        self.assertEqual(User.objects.count(), 0)

    def test_post_no_username(self):
        data = {'email':'bad_mail', 'password':'test_password', 'usertype': 0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('signup'), 1)
        self.assertEqual(User.objects.count(), 0)

    def test_post_no_usertype(self):
        data = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('signup'), 1)
        self.assertEqual(User.objects.count(), 0)


class UsernameTests(APITestCase):

    url = userpage_url + 'username'

    def test_get_unused(self):
        data = {'username': 'test_username'}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('used'), 0)

    def test_get_used(self):
        data = {'username': 'test_username'}
        test_user = User()
        test_user.username = data['username']
        test_user.save()
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data.get('used'), 1)


class EmailTests(APITestCase):

    url = userpage_url + 'email'

    def test_get_unused(self):
        data = {'email': 'test_email@test.com'}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email_used'), 0)

    def test_get_used(self):
        data = {'email': 'test_email@test.com'}
        test_user = User()
        test_user.email = data['email']
        test_user.save()
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data.get('email_used'), 1)


class LoginTests(APITestCase):

    url = userpage_url + 'login'

    def test_get_not_logged(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('login'), 0)

    def test_get_logged_without_usertype(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        self.client.login(username=data_prepare['username'], password=data_prepare['password'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('login'), 0)

    def test_get_logged_contestant(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'usertype':'0'}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_contestant = ContestantUser()
        test_contestant.user = test_user
        test_contestant.save()
        test_user.first_name = 'contestant'
        test_user.save()
        self.client.login(username=data_prepare['username'], password=data_prepare['password'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('login'), 1)

    def test_get_logged_organizer(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'usertype':'1'}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user.first_name = 'organizer'
        test_user.save()
        self.client.login(username=data_prepare['username'], password=data_prepare['password'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('login'), 1)

    def test_post_log_contestant(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'usertype':'0'}
        data = {'username': data_prepare['username'], 'password': data_prepare['password']}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_contestant = ContestantUser()
        test_contestant.user = test_user
        test_contestant.save()
        test_user.first_name = 'contestant'
        test_user.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('login'), 0)
        self.assertEqual(response.data.get('usertype'), int(data_prepare['usertype']))

    def test_post_log_organizer(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'usertype':'1'}
        data = {'username': data_prepare['username'], 'password': data_prepare['password']}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user.first_name = 'organizer'
        test_user.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('login'), 0)
        self.assertEqual(response.data.get('usertype'), int(data_prepare['usertype']))

    def test_post_log_wrong_username(self):
        data = {'username': 'test_username', 'password': 'test_password'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('login'), 1)

    def test_post_log_wrong_password(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'usertype':'1'}
        data = {'username': data_prepare['username'], 'password': 'wrong_password'}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user.first_name = 'organizer'
        test_user.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('login'), 1)

    def test_post_log_without_usertype(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data = {'username': data_prepare['username'], 'password': data_prepare['password']}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('login'), 1)


class LogoutTests(APITestCase):

    url = userpage_url + 'logout'

    def test_get_not_logged(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('logout'), 0)

    def test_get_logged(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        self.client.login(username=data_prepare['username'], password=data_prepare['password'])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('logout'), 1)


class ForgetPasswordTests(APITestCase):

    url = userpage_url + 'forget_password'

    def test_post_success(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data = {'email': data_prepare['email']}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['encode_string'], None)

    def test_post_wrong_email(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data = {'email': 'wrong_email'}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ChangePasswordTests(APITestCase):

    url = userpage_url + 'change_password'

    def test_post_success(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'encode_id':'test_encode_id'}
        data = {'encode_id': data_prepare['encode_id'], 'password':'new_password'}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_password_token = PasswordToken()
        test_password_token.username_token = data_prepare['encode_id']
        test_password_token.username = data_prepare['username']
        test_password_token.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_no_encode_id(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'encode_id':'test_encode_id'}
        data = {'password':'new_password'}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_password_token = PasswordToken()
        test_password_token.username_token = data_prepare['encode_id']
        test_password_token.username = data_prepare['username']
        test_password_token.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_wrong_encode_id(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'encode_id':'test_encode_id'}
        data = {'encode_id': 'wrong_encode_id', 'password': 'new_password'}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_password_token = PasswordToken()
        test_password_token.username_token = data_prepare['encode_id']
        test_password_token.username = data_prepare['username']
        test_password_token.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ValidateEmailTests(APITestCase):

    url = userpage_url + 'validate_email'

    def test_post_success(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'encode_id':'test_encode_id'}
        data = {'encode_id': data_prepare['encode_id']}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_email_token = EmailToken()
        test_email_token.username_token = data_prepare['encode_id']
        test_email_token.username = data_prepare['username']
        test_email_token.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['validate'], 1)

    def test_post_success_again(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'encode_id':'test_encode_id'}
        data = {'encode_id': data_prepare['encode_id']}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.last_name = '1'
        test_user.save()
        test_email_token = EmailToken()
        test_email_token.username_token = data_prepare['encode_id']
        test_email_token.username = data_prepare['username']
        test_email_token.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['validate'], 2)

    def test_post_no_encode_id(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'encode_id':'test_encode_id'}
        data = {}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.last_name = '1'
        test_user.save()
        test_email_token = EmailToken()
        test_email_token.username_token = data_prepare['encode_id']
        test_email_token.username = data_prepare['username']
        test_email_token.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_wrong_encode_id(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password', 'encode_id':'test_encode_id'}
        data = {'encode_id': 'wrong_encode_id', 'password': 'new_password'}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.last_name = '1'
        test_user.save()
        test_email_token = EmailToken()
        test_email_token.username_token = data_prepare['encode_id']
        test_email_token.username = data_prepare['username']
        test_email_token.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ConDetailTests(APITestCase):

    url = userpage_url + 'con_detail'

    def test_get(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data_prepare_contestant = {'name': 'test_name', 'nickname': 'test_nickname', 'gender': 0,
                                   'introduction': 'test_introduction', 'school': 'test_school', 'major': 'test_major',
                                   'student_number': 'test_student_number', 'phone_number': 'test_phone_number', 'avatar_url': ''}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.first_name = 'contestant'
        test_user.save()
        serializer = ContestantUserSerializer(data=data_prepare_contestant)
        if serializer.is_valid():
            serializer.save(user=test_user)
        response = self.client.get(self.url + '/' + str(serializer.data['id']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_success(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data_prepare_contestant = {'name': 'test_name', 'nickname': 'test_nickname', 'gender': 0,
                                   'introduction': 'test_introduction', 'school': 'test_school', 'major': 'test_major',
                                   'student_number': 'test_student_number', 'phone_number': 'test_phone_number', 'avatar_url': ''}
        data = {'name': 'new_name', 'nickname': 'new_nickname', 'gender': 1,
                'introduction': 'test_introduction', 'school': 'test_school', 'major': 'test_major',
                'student_number': 'test_student_number', 'phone_number': 'test_phone_number', 'avatar_url': ''}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.first_name = 'contestant'
        test_user.save()
        serializer = ContestantUserSerializer(data=data_prepare_contestant)
        if serializer.is_valid():
            serializer.save(user=test_user)
        serializer_new = ContestantUserSerializer(data=data)
        self.client.login(username=data_prepare['username'], password=data_prepare['password'])
        response = self.client.post(self.url + '/' + str(serializer.data['id']), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_post_not_logged(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data_prepare_contestant = {'name': 'test_name', 'nickname': 'test_nickname', 'gender': 0,
                                   'introduction': 'test_introduction', 'school': 'test_school', 'major': 'test_major',
                                   'student_number': 'test_student_number', 'phone_number': 'test_phone_number', 'avatar_url': ''}
        data = {'name': 'new_name', 'nickname': 'new_nickname', 'gender': 1,
                'introduction': 'test_introduction', 'school': 'test_school', 'major': 'test_major',
                'student_number': 'test_student_number', 'phone_number': 'test_phone_number', 'avatar_url': ''}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.first_name = 'contestant'
        test_user.save()
        serializer = ContestantUserSerializer(data=data_prepare_contestant)
        if serializer.is_valid():
            serializer.save(user=test_user)
        serializer_new = ContestantUserSerializer(data=data)
        response = self.client.post(self.url + '/' + str(serializer.data['id']), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_wrong_logged(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
        data_prepare_contestant = {'name': 'test_name', 'nickname': 'test_nickname', 'gender': 0,
                                   'introduction': 'test_introduction', 'school': 'test_school', 'major': 'test_major',
                                   'student_number': 'test_student_number', 'phone_number': 'test_phone_number', 'avatar_url': ''}
        data = {'name': 'new_name', 'nickname': 'new_nickname', 'gender': 1,
                'introduction': 'test_introduction', 'school': 'test_school', 'major': 'test_major',
                'student_number': 'test_student_number', 'phone_number': 'test_phone_number', 'avatar_url': ''}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.first_name = 'contestant'
        test_user.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'], email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        serializer = ContestantUserSerializer(data=data_prepare_contestant)
        if serializer.is_valid():
            serializer.save(user=test_user)
        serializer_new = ContestantUserSerializer(data=data)
        self.client.login(username=data_prepare2['username'], password=data_prepare2['password'])
        response = self.client.post(self.url + '/' + str(serializer.data['id']), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrgDetailTests(APITestCase):

    url = userpage_url + 'org_detail'

    def test_get(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data_prepare_organizer = {'name': 'test_name', 'shortname': 'test_shortname', 'introduction': 'test_introduction',
                                   'address': 'test_address', 'field': 'test_field', 'contact': 'test_contact',
                                   'contact_number': 'test_number', 'contact_email': 'test_email', 'avatar_url': ''}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        serializer = OrganizerUserSerializer(data=data_prepare_organizer)
        if serializer.is_valid():
            serializer.save(user=test_user)
        response = self.client.get(self.url + '/' + str(serializer.data['id']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_success(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data_prepare_organizer = {'name': 'test_name', 'shortname': 'test_shortname', 'introduction': 'test_introduction',
                                   'address': 'test_address', 'field': 'test_field', 'contact': 'test_contact',
                                   'contact_number': 'test_number', 'contact_email': 'test_email', 'avatar_url': ''}
        data = {'name': 'new_name', 'shortname': 'test_shortname', 'introduction': 'test_introduction',
                'address': 'test_address', 'field': 'test_field', 'contact': 'test_contact',
                'contact_number': 'test_number', 'contact_email': 'test_email', 'avatar_url': ''}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        serializer = OrganizerUserSerializer(data=data_prepare_organizer)
        if serializer.is_valid():
            serializer.save(user=test_user)
        serializer_new = OrganizerUserSerializer(data=data)
        self.client.login(username=data_prepare['username'], password=data_prepare['password'])
        response = self.client.post(self.url + '/' + str(serializer.data['id']), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_post_not_logged(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data_prepare_organizer = {'name': 'test_name', 'shortname': 'test_shortname', 'introduction': 'test_introduction',
                                   'address': 'test_address', 'field': 'test_field', 'contact': 'test_contact',
                                   'contact_number': 'test_number', 'contact_email': 'test_email', 'avatar_url': ''}
        data = {'name': 'new_name', 'shortname': 'test_shortname', 'introduction': 'test_introduction',
                'address': 'test_address', 'field': 'test_field', 'contact': 'test_contact',
                'contact_number': 'test_number', 'contact_email': 'test_email', 'avatar_url': ''}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        serializer = OrganizerUserSerializer(data=data_prepare_organizer)
        if serializer.is_valid():
            serializer.save(user=test_user)
        serializer_new = OrganizerUserSerializer(data=data)
        response = self.client.post(self.url + '/' + str(serializer.data['id']), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_wrong_logged(self):
        data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
        data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
        data_prepare_organizer = {'name': 'test_name', 'shortname': 'test_shortname', 'introduction': 'test_introduction',
                                   'address': 'test_address', 'field': 'test_field', 'contact': 'test_contact',
                                   'contact_number': 'test_number', 'contact_email': 'test_email', 'avatar_url': ''}
        data = {'name': 'new_name', 'shortname': 'test_shortname', 'introduction': 'test_introduction',
                'address': 'test_address', 'field': 'test_field', 'contact': 'test_contact',
                'contact_number': 'test_number', 'contact_email': 'test_email', 'avatar_url': ''}
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'], email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'], email=data_prepare2['email'])
        test_user2.first_name = 'organizer'
        test_user2.save()
        serializer = OrganizerUserSerializer(data=data_prepare_organizer)
        if serializer.is_valid():
            serializer.save(user=test_user)
        serializer_new = OrganizerUserSerializer(data=data)
        self.client.login(username=data_prepare2['username'], password=data_prepare2['password'])
        response = self.client.post(self.url + '/' + str(serializer.data['id']), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AvatarUploadTests(APITestCase):

    url = userpage_url + 'avatar_upload'

    def test_post(self):
        self.assertEqual(1, 1)


class MyCompetitionTests(APITestCase):

    url = userpage_url + 'competition'
    data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
    data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
    test_competition_name = 'test_competition'

    def init_test(self, data):
        data_prepare = self.data_prepare
        data_prepare2 = self.data_prepare2
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'],
                                             email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'],
                                              email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        test_contestant = ContestantUser()
        test_contestant.user = test_user2
        test_contestant.save()
        test_competition = Competition()
        test_competition.organizer = test_organizer
        test_competition.save()
        if data.get('status') == '0':
            test_competition.followers.add(test_contestant)
        elif data.get('status') == '1':
            test_competition.joiners.add(test_contestant)
        test_competition.name = self.test_competition_name
        test_competition.save()

    def test_get_status_organizer(self):
        data = {'status': '0'}
        self.init_test(data)
        self.client.login(username=self.data_prepare['username'], password=self.data_prepare['password'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('competitions')[0]['name'], self.test_competition_name)

    def test_get_status_0(self):
        data = {'status': '0'}
        self.init_test(data)
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('competitions')[0]['name'], self.test_competition_name)

    def test_get_status_not_0(self):
        data = {'status': '1'}
        self.init_test(data)
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('competitions')[0]['name'], self.test_competition_name)

    def test_get_not_logged(self):
        data = {'status': '0'}
        self.init_test(data)
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CollectCompetitionTests(APITestCase):

    url = userpage_url + 'collect_competition'
    data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
    data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
    data_prepare_competiton = {'name': 'test_competition_name', 'id': 0}

    def init_test(self, data):
        data_prepare = self.data_prepare
        data_prepare2 = self.data_prepare2
        data_prepare_competition = self.data_prepare_competiton
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'],
                                             email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'],
                                              email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        test_contestant = ContestantUser()
        test_contestant.user = test_user2
        test_contestant.save()
        test_competition = Competition()
        test_competition.name = data_prepare_competition['name']
        test_competition.organizer = test_organizer
        test_competition.save()
        self.data_prepare_competiton['id'] = test_competition.id
        if data.get('status') == '0':
            test_competition.followers.add(test_contestant)
            test_competition.save()

    def test_post_follow(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'competition_id': self.data_prepare_competiton['id'], 'status': '1'}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_competition = Competition.objects.get(name=self.data_prepare_competiton['name'])
        self.assertEqual(test_competition.followers.count(), 1)
        test_contestant = User.objects.get(username=self.data_prepare2['username']).contestant_user
        self.assertEqual(CompetitionAndContestant.objects.filter(competition=test_competition, contestant=test_contestant).count(), 1)

    def test_post_unfollow(self):
        data_init = {'status': '0'}
        self.init_test(data_init)
        data = {'competition_id': self.data_prepare_competiton['id'], 'status': '0'}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Competition.objects.get(name=self.data_prepare_competiton['name']).followers.count(), 0)

    def test_post_follow_followed(self):
        data_init = {'status': '0'}
        self.init_test(data_init)
        data = {'competition_id': self.data_prepare_competiton['id'], 'status': '1'}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Competition.objects.get(name=self.data_prepare_competiton['name']).followers.count(), 1)

    def test_post_unfollow_unfollowed(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'competition_id': self.data_prepare_competiton['id'], 'status': '0'}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Competition.objects.get(name=self.data_prepare_competiton['name']).followers.count(), 0)

    def test_post_not_logged(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'competition_id': self.data_prepare_competiton['id'], 'status': '1'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Competition.objects.get(name=self.data_prepare_competiton['name']).followers.count(), 0)

    def test_post_no_id(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'status': '1'}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Competition.objects.get(name=self.data_prepare_competiton['name']).followers.count(), 0)


class CollectTutorialTests(APITestCase):

    url = userpage_url + 'collect_tutorial'
    data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
    data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
    data_prepare_tutorial = {'title': 'test_tutorial_title', 'id': 0}

    def init_test(self, data):
        data_prepare = self.data_prepare
        data_prepare2 = self.data_prepare2
        data_prepare_tutorial = self.data_prepare_tutorial
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'],
                                             email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'],
                                              email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        test_contestant = ContestantUser()
        test_contestant.user = test_user2
        test_contestant.save()
        test_tutorial = Tutorial()
        test_tutorial.title = data_prepare_tutorial['title']
        test_tutorial.author = test_organizer.user
        test_tutorial.save()
        self.data_prepare_tutorial['id'] = test_tutorial.id
        if data.get('status') == '0':
            test_tutorial.collectors.add(test_contestant)
            test_tutorial.save()

    def test_post_follow(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'tutorial_id': self.data_prepare_tutorial['id'], 'status': '1'}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tutorial.objects.get(title=self.data_prepare_tutorial['title']).collectors.count(), 1)

    def test_post_unfollow(self):
        data_init = {'status': '0'}
        self.init_test(data_init)
        data = {'tutorial_id': self.data_prepare_tutorial['id'], 'status': '0'}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tutorial.objects.get(title=self.data_prepare_tutorial['title']).collectors.count(), 0)

    def test_post_follow_followed(self):
        data_init = {'status': '0'}
        self.init_test(data_init)
        data = {'tutorial_id': self.data_prepare_tutorial['id'], 'status': '1'}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tutorial.objects.get(title=self.data_prepare_tutorial['title']).collectors.count(), 1)

    def test_post_unfollow_unfollowed(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'tutorial_id': self.data_prepare_tutorial['id'], 'status': '0'}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tutorial.objects.get(title=self.data_prepare_tutorial['title']).collectors.count(), 0)

    def test_post_not_logged(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'tutorial_id': self.data_prepare_tutorial['id'], 'status': '1'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Tutorial.objects.get(title=self.data_prepare_tutorial['title']).collectors.count(), 0)

    def test_post_no_id(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'status': '1'}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Tutorial.objects.get(title=self.data_prepare_tutorial['title']).collectors.count(), 0)


class IsTutorialTests(APITestCase):

    url = userpage_url + 'is_tutorial'
    data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
    data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
    data_prepare_tutorial = {'title': 'test_tutorial_title', 'id': 0}

    def init_test(self, data):
        data_prepare = self.data_prepare
        data_prepare2 = self.data_prepare2
        data_prepare_tutorial = self.data_prepare_tutorial
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'],
                                             email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'],
                                              email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        test_contestant = ContestantUser()
        test_contestant.user = test_user2
        test_contestant.save()
        test_tutorial = Tutorial()
        test_tutorial.title = data_prepare_tutorial['title']
        test_tutorial.author = test_organizer.user
        test_tutorial.save()
        self.data_prepare_tutorial['id'] = test_tutorial.id
        if data.get('status') == '1':
            test_tutorial.collectors.add(test_contestant)
            test_tutorial.save()

    def test_get_followed(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'tutorial_id': self.data_prepare_tutorial['id']}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('tutorial_status'), 1)

    def test_get_unfollowed(self):
        data_init = {'status': '0'}
        self.init_test(data_init)
        data = {'tutorial_id': self.data_prepare_tutorial['id']}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('tutorial_status'), 0)

    def test_get_no_tutorial_id(self):
        data_init = {'status': '0'}
        self.init_test(data_init)
        data = {}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_not_logged(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'tutorial_id': self.data_prepare_tutorial['id']}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_wrong_logged(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {'tutorial_id': self.data_prepare_tutorial['id']}
        self.client.login(username=self.data_prepare['username'], password=self.data_prepare['password'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MyPersonalLetterTests(APITestCase):

    url = userpage_url + 'personal_letter'
    data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
    data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
    data_prepare_letter = {'content': 'test_content', 'id': 0}

    def init_test(self, data):
        data_prepare = self.data_prepare
        data_prepare2 = self.data_prepare2
        data_prepare_letter = self.data_prepare_letter
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'],
                                             email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'],
                                              email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        test_contestant = ContestantUser()
        test_contestant.user = test_user2
        test_contestant.save()
        if data.get('status') == '1':
            test_letter = PersonalLetter()
            test_letter.title = data_prepare_letter['content']
            test_letter.sender = test_user
            test_letter.receiver = test_user2
            test_letter.is_read = 0
            test_letter.save()
            self.data_prepare_letter['id'] = test_letter.id

    def test_get_sender(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {}
        self.client.login(username=self.data_prepare['username'], password=self.data_prepare['password'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_user2 = User.objects.get(username=self.data_prepare2['username'])
        self.assertEqual(len(response.data.get('receivers')), 1)
        self.assertEqual(response.data.get('receivers')[0]['author']['id'], test_user2.id)

    def test_get_receiver(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {}
        self.client.login(username=self.data_prepare2['username'], password=self.data_prepare2['password'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_user = User.objects.get(username=self.data_prepare['username'])
        self.assertEqual(len(response.data.get('receivers')), 1)
        self.assertEqual(response.data.get('receivers')[0]['author']['id'], test_user.id)

    def test_get_not_logged(self):
        data_init = {'status': '1'}
        self.init_test(data_init)
        data = {}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_success(self):
        data_init = {'status': '0'}
        self.init_test(data_init)
        data = {'id': User.objects.get(username=self.data_prepare2['username']).id,
                'content': self.data_prepare_letter['content']}
        self.client.login(username=self.data_prepare['username'], password=self.data_prepare['password'])
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('return_code'), 1)
        self.assertEqual(PersonalLetter.objects.count(), 1)
        test_user = User.objects.get(username=self.data_prepare['username'])
        test_user2 = User.objects.get(username=self.data_prepare2['username'])
        self.assertEqual(PersonalLetter.objects.get(sender=test_user).content, self.data_prepare_letter['content'])
        self.assertEqual(PersonalLetter.objects.get(receiver=test_user2).content, self.data_prepare_letter['content'])

    def test_post_not_logged(self):
        data_init = {'status': '0'}
        self.init_test(data_init)
        data = {'id': User.objects.get(username=self.data_prepare2['username']).id,
                'content': self.data_prepare_letter['content']}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LetterDetailTests(APITestCase):

    url = userpage_url + 'letter_detail'
    data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
    data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
    data_prepare_letter = {'content': 'test_content', 'id': 0}

    def init_test(self, data):
        data_prepare = self.data_prepare
        data_prepare2 = self.data_prepare2
        data_prepare_letter = self.data_prepare_letter
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'],
                                             email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'],
                                              email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        test_contestant = ContestantUser()
        test_contestant.user = test_user2
        test_contestant.save()
        test_letter = PersonalLetter()
        test_letter.content = data_prepare_letter['content']
        test_letter.sender = test_user
        test_letter.receiver = test_user2
        test_letter.is_read = 0
        test_letter.save()
        self.data_prepare_letter['id'] = test_letter.id

    def test_get(self):
        data_init = {}
        self.init_test(data_init)
        data = {'id': User.objects.get(username=self.data_prepare2['username']).id}
        self.client.login(username=self.data_prepare['username'], password=self.data_prepare['password'])
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data.get('our_letters')), 1)
        self.assertEqual(response.data.get('our_letters')[0]['content'], self.data_prepare_letter['content'])

    def test_get_not_logged(self):
        data_init = {}
        self.init_test(data_init)
        data = {'id': User.objects.get(username=self.data_prepare2['username']).id}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OtherContestantCompetitionTests(APITestCase):

    url = userpage_url + 'other_contestant_competition'
    data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
    data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
    data_prepare_competition = {'name': 'test_competition_name', 'id': 0}

    def init_test(self, data):
        data_prepare = self.data_prepare
        data_prepare2 = self.data_prepare2
        data_prepare_competition = self.data_prepare_competition
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'],
                                             email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'],
                                              email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        test_contestant = ContestantUser()
        test_contestant.user = test_user2
        test_contestant.save()
        test_competition = Competition()
        test_competition.organizer = test_organizer
        test_competition.save()
        test_competition.followers.add(test_contestant)
        test_competition.joiners.add(test_contestant)
        test_competition.name = data_prepare_competition['name']
        self.data_prepare_competition['id'] = test_competition.id
        test_competition.save()

    def test_get_success(self):
        data_init = {}
        self.init_test(data_init)
        data = {'id': User.objects.get(username=self.data_prepare2['username']).contestant_user.id}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_no_id(self):
        data_init = {}
        self.init_test(data_init)
        data = {}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OtherOrganizerCompetitionTests(APITestCase):
    url = userpage_url + 'other_organizer_competition'
    data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
    data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
    data_prepare_competition = {'name': 'test_competition_name', 'id': 0}

    def init_test(self, data):
        data_prepare = self.data_prepare
        data_prepare2 = self.data_prepare2
        data_prepare_competition = self.data_prepare_competition
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'],
                                             email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'],
                                              email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        test_contestant = ContestantUser()
        test_contestant.user = test_user2
        test_contestant.save()
        test_competition = Competition()
        test_competition.organizer = test_organizer
        test_competition.save()
        test_competition.followers.add(test_contestant)
        test_competition.joiners.add(test_contestant)
        test_competition.name = data_prepare_competition['name']
        self.data_prepare_competition['id'] = test_competition.id
        test_competition.save()

    def test_get_success(self):
        data_init = {}
        self.init_test(data_init)
        data = {'id': User.objects.get(username=self.data_prepare['username']).organizer_user.id}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_no_id(self):
        data_init = {}
        self.init_test(data_init)
        data = {}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OtherContestantTutorialTests(APITestCase):
    url = userpage_url + 'other_contestant_tutorial'
    data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
    data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
    data_prepare_tutorial = {'title': 'test_tutorial_title', 'id': 0}

    def init_test(self, data):
        data_prepare = self.data_prepare
        data_prepare2 = self.data_prepare2
        data_prepare_tutorial = self.data_prepare_tutorial
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'],
                                             email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'],
                                              email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        test_contestant = ContestantUser()
        test_contestant.user = test_user2
        test_contestant.save()
        test_tutorial = Tutorial()
        test_tutorial.title = data_prepare_tutorial['title']
        test_tutorial.author = test_contestant.user
        test_tutorial.save()
        self.data_prepare_tutorial['id'] = test_tutorial.id
        test_tutorial.collectors.add(test_contestant)
        test_tutorial.save()

    def test_get_success(self):
        data_init = {}
        self.init_test(data_init)
        data = {'id': User.objects.get(username=self.data_prepare2['username']).contestant_user.id}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_no_id(self):
        data_init = {}
        self.init_test(data_init)
        data = {}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OtherOrganizerTutorialTests(APITestCase):
    url = userpage_url + 'other_organizer_tutorial'
    data_prepare = {'username': 'test_username', 'email': 'test_email@test.com', 'password': 'test_password'}
    data_prepare2 = {'username': 'test_username2', 'email': 'test_email2@test.com', 'password': 'test_password2'}
    data_prepare_tutorial = {'title': 'test_tutorial_title', 'id': 0}

    def init_test(self, data):
        data_prepare = self.data_prepare
        data_prepare2 = self.data_prepare2
        data_prepare_tutorial = self.data_prepare_tutorial
        test_user = User.objects.create_user(username=data_prepare['username'], password=data_prepare['password'],
                                             email=data_prepare['email'])
        test_user.first_name = 'organizer'
        test_user.save()
        test_organizer = OrganizerUser()
        test_organizer.user = test_user
        test_organizer.save()
        test_user2 = User.objects.create_user(username=data_prepare2['username'], password=data_prepare2['password'],
                                              email=data_prepare2['email'])
        test_user2.first_name = 'contestant'
        test_user2.save()
        test_contestant = ContestantUser()
        test_contestant.user = test_user2
        test_contestant.save()
        test_tutorial = Tutorial()
        test_tutorial.title = data_prepare_tutorial['title']
        test_tutorial.author = test_organizer.user
        test_tutorial.save()
        self.data_prepare_tutorial['id'] = test_tutorial.id
        test_tutorial.collectors.add(test_contestant)
        test_tutorial.save()

    def test_get_success(self):
        data_init = {}
        self.init_test(data_init)
        data = {'id': User.objects.get(username=self.data_prepare['username']).organizer_user.id}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_no_id(self):
        data_init = {}
        self.init_test(data_init)
        data = {}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)