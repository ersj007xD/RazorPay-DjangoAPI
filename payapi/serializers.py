from rest_framework.response import Response
from xml.dom import VALIDATION_ERR, ValidationErr
from rest_framework import serializers
from .models import Coffee, User
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password is not matched')
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ['email', 'password']


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']                 

class CofeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = ['id', 'name', 'amount', 'payment_id', 'paid']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=1000, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=1000, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password is not matched')
        user.set_password(password)
        user.save()    
        return data        

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=400)
    class Meta:
        fields = ['email']

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:8000/api/user/reset/'+uid+'/'+token
            print("UID", uid)
            print("token", token)
            return data
        else:
            raise ValidationErr("You are not registered user")  

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=1000, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=1000, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, data):
        try:
            password = data.get('password')
            password2 = data.get('password2')
            uid= self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('Password is not matched')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationErr("Token is not valid or Expired !")

            user.set_password(password)
            user.save()    
            return data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationErr("Token is not valid or Expired !")    



