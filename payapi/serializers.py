from rest_framework import serializers
from .models import Coffee, User

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