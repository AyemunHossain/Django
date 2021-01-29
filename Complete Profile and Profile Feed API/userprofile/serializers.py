from rest_framework import serializers
from userprofile.models import ProfileFeedItem, Account

class ProfileSerializers(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ("id","email","username","first_name","last_name","password")
		extra_kwargs = {
			'password':{
				'write_only': True,
				'style': {'input_type':'password'}
			}
		}

	def create(self, validate_data):
		user = models.Account.objects.create_user(
				email = validate_data['email'],
				username = validate_data['username'],
				first_name = validate_data['first_name'],
				last_name = validate_data['last_name'],
				password = validate_data['password'],
			)
		return user

class ProfileFeedItemSerializer(serializers.ModelSerializer):

	class Meta:
		model = ProfileFeedItem
		fields = ('id','user_profile','status_text','created')
		extra_kwargs = {'user_profile':{'read_only':True}}
		