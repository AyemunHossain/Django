from django.test import TestCase
from app.calculator import add, sub, mul, div

class CalculatorTest(TestCase):
	def test_add(self):
		"""Test that two numbers are added together"""
		self.assertEqual(add(2,3),5)