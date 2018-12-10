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
            'profile',
            'category',
            'amount'
        ]

class ExpensesSerializer(serializers.ModelSerializer):
    budget = BudgetSerializer()
    class Meta:
        model = Expenses
        fields=[
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