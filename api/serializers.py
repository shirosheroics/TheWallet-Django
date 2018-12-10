from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (Budget, Expenses, Profile )

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data

class UserLoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField(write_only=True)
	token = serializers.CharField(allow_blank=True, read_only=True)

	def validate(self, data):
		my_username = data.get('username')
		my_password = data.get('password')

		try:
			user_obj = User.objects.get(username=my_username)
			jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
			jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

			payload = jwt_payload_handler(user_obj)
			token = jwt_encode_handler(payload)

			data["token"] = token
		except:
			raise serializers.ValidationError("This username does not exist")

		if not user_obj.check_password(my_password):
			raise serializers.ValidationError("Incorrect username/password combination! Noob..")
		return data

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [  
		'username',
		'first_name',
		'last_name',
		'email'
			]

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Profile
		fields = [  
		'user',
        'id',
		'phoneNo',
		'dob',
		'gender',
		'income'
			]

class BudgetSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Budget
        fields = [
            'id',
            'profile',
            'label',
            'category',
            'amount'
        ]

class ExpensesSerializer(serializers.ModelSerializer):
    budget = BudgetSerializer()
    class Meta:
        model = Expenses
        fields=[
            'id',
            'budget',
            'amount',
            'label',
            'date',
            'occurances'
        ]

class BudgetCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = [
            'profile',
            'label',
            'category',
            'amount'
        ]

class BudgetAmountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = [
            'amount'
        ]

class ExpensesCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields=[
            'budget',
            'amount',
            'label',
            'date',
            'occurances'
        ]