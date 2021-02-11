from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):

	def test_create_user_with_email(self):
		"""Testing creating a new user with an email"""
		email = "ah@gmail.com"
		password = 'testpass1'
		user = get_user_model().objects.create_user(
			email = email,
			password = password,)
		self.assertEqual(user.email, email)
		self.assertTrue(user.check_password(password))

	def test_create_user_with_username(self):
		"""Testing creating user with username"""
		payload = {	"username" : "ashik1",
                    "password" : "123a123r"}
		with self.assertRaises(TypeError,):
			user = get_user_model().objects.create_user(**payload)
	
	def test_create_superuser(self):
		"""Testing the superuser account creation"""
		payload = {"email": "ah@gmail.com", "password" :'testpass1'}
		user = get_user_model().objects.create_user(**payload)
		self.assertEqual(user.email, payload["email"])
		self.assertTrue(user.check_password(payload["password"]))
		
	def test_create_superuser_without_password(self):
		"""Testing the superuser account creation"""
		payload = {"email": "ah@gmail.com",}
		with self.assertRaises(TypeError):
			user = get_user_model().objects.create_user(**payload)
			self.assertEqual(user.email, payload["password"])
