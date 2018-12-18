from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (Budget, Transaction, Profile , Expense, Goal, Deposit)

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

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields=[
			'id',
			'user',
			'budget',
			'amount',
			'label',
			'date',
		]

class BudgetSerializer(serializers.ModelSerializer):
	transactions = TransactionSerializer(many=True, read_only=True)
	class Meta:
		model = Budget
		fields = [
			'id',
			'profile',
			'label',
			'category',
			'amount',
			'balance',
			'date',
			'transactions'
		]

class DepositSerializer(serializers.ModelSerializer):
	class Meta:
		model = Deposit
		fields=[
			'id',
			'goal',
			'amount',
			'date',
		]

class GoalSerializer(serializers.ModelSerializer):
	deposits = DepositSerializer(many=True, read_only=True)
	class Meta:
		model = Goal
		fields = [
			'id',
			'profile',
			'label',
			'end_date',
			'amount',
			'description',
			'balance',
			'deposits'
		]

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	budgets= BudgetSerializer(many=True, read_only=True)
	goals=GoalSerializer(many=True, read_only=True)
	class Meta:
		model = Profile
		fields = [  
		'user',
		'id',
		'phoneNo',
		'dob',
		'gender',
		'income',
		'balance',
		'savings',
		'automated',
		'budgets',
		'goals'
			]

class ProfileCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = [  
		'phoneNo',
		'dob',
		'gender',
		'balance',
		'savings',
		'automated',
		'income'
			]

class ExpenseSerializer(serializers.ModelSerializer):
	# profile = ProfileSerializer()
	class Meta:
		model = Expense
		fields = [
			'id',
			'profile',
			'label',
			'amount'
		]


class BudgetCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Budget
		fields = [
			'id',
			'profile',
			'label',
			'category',
			'balance',
			'amount'
		]

class GoalCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Goal
		fields = [
			'id',
			'profile',
			'label',
			'end_date',
			'amount',
			'description',
			'balance'
		]

class ExpenseCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Expense
		fields = [
			'profile',
			'label',
			'amount'
		]


class TransactionCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields=[
			'user',
			'budget',
			'amount',
			'label',
			'date'
		]

class DepositCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Deposit
		fields=[
			'goal',
			'amount'
		]