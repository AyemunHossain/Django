from django.test import TestCase
from django.contrib.auth.models import User

class ModelTest(TestCase):

	def test_create_user_with_email(self):
		"""Testing creating a new user with an email"""
		with self.assertRaises(TypeError):
			email = "ah@gmail.com"
			password = 'testpass1'
			user = User.objects.create_user(
				email = email,
				password = password,)
			self.assertEqual(user.email, email)
			self.assertTrue(user.check_password(password))

	def test_create_user_with_username(self):
		username = "ashik1"
		password = "123a123r"

		user = User.objects.create_user(
			username = username,
			password = password,)