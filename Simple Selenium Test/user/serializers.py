from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','email','password']
        extra_kwargs = {
            'id':{
                'read_only':True,
            },
            'password': {
                'write_only': True,
                'min_length':8,
                'style': {'input_type': 'password'}
            }
        }
    
    def create(self, validate_data):
        user = get_user_model().objects.create_user(
                email = validate_data['email'],
                password = validate_data['password'],)
        return user

class AuthTokenSerializser(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace = False,
    )

    def validate(self, attrs):
        """Validated and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,)
            
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
