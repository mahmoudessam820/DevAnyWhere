from django.contrib.auth import authenticate
from django.test import TestCase, Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from rest_framework import status 
from django.contrib.auth import get_user_model



from .views import login_view, signup_view



CustomUser = get_user_model()


class LoginViewTestCase(TestCase):

	def setUp(self):

		self.client = Client()
		self.factory = RequestFactory()
		self.url = reverse('login')
		self.username = 'amr'
		self.password1 = 'testpass123'
		self.user = CustomUser.objects.create_user(username=self.username, password=self.password1)

		# Add session middleware to the factory
		session_middleware = SessionMiddleware(lambda x: None)
		self.request = self.factory.post(self.url, {'username': self.username, 'password1': self.password1}, format='json')
		session_middleware.process_request(self.request)
		self.request.session.save()


	def test_valid_login(self):

		response = login_view(self.request)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('message', response.data)


	def test_invalid_login(self):

		post_data = self.request.POST.copy()
		post_data['username'] = 'tony'
		post_data['password'] = '12346789'

		# Set the request's POST data to the modified data
		self.request.POST = post_data

		response = login_view(self.request)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertIn('message', response.data)


class SignupViewTestCase(TestCase):

	def setUp(self):

		self.factory = RequestFactory()
		self.user = CustomUser
		self.url = reverse('signup')


	def test_signup_success(self):

		data = {

			"username":"alx",
			"email":"alx@example.com",
			"password1":"alxtpass123",
			"password2":"alxtpass123"

		}

		request = self.factory.post(self.url, data=data)
		middleware = SessionMiddleware(lambda x: None)
		middleware.process_request(request)

		response = signup_view(request)

		# Check if user is created and authenticated
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(self.user.objects.filter(username=data['username']).exists())
		user = authenticate(username=data['username'], password=data['password1'])
		self.assertIsNotNone(user)
		self.assertEqual(user.username, data['username'])


	def test_signup_failure(self):


		data = {

		    'username': '',  # invalid empty value
		    'email': 'invalid-email',  # invalid email format
		    'password1': '123',  # too short
		    'password2': '456',  # doesn't match password1
		}


		request = self.factory.post(self.url, data=data)
		middleware = SessionMiddleware(lambda x: None)
		middleware.process_request(request)

		response = signup_view(request)

		# Check if error response is returned with form validation errors
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertTrue('errors' in response.data)
		errors = response.data['errors']
		self.assertTrue('username' in errors)
		self.assertTrue('email' in errors)
		self.assertTrue('password2' in errors)