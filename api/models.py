
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
	GENDER_CHOICE = (
		('Female', 'Female'),
		('Male', 'Male'),
		)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phoneNo = models.CharField(max_length=9,null=True)
	dob = models.DateField(null=True)
	gender=models.CharField(max_length=6, choices=GENDER_CHOICE, null=True)
	income=models.IntegerField(null=True)
	balance = models.DecimalField( max_digits=10, decimal_places=3, null=True)
	savings = models.DecimalField( max_digits=10, decimal_places=3, null=True)
	automated = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

class Budget(models.Model):
	TYPE_CHOICE = (
		('Food', 'Food'),
		('Health', 'Health'),
		('Personal', 'Personal'),
		('Emergency', 'Emergency'),
		('Entertainment', 'Entertainment'),
		('Transportation', 'Transportation'),
		('Others', 'Others')
	)

	profile= models.ForeignKey(Profile, default=1, related_name='budgets',  on_delete=models.CASCADE)
	label=models.CharField(max_length=120)
	category = models.CharField(max_length=13, choices=TYPE_CHOICE)
	amount = models.DecimalField( max_digits=10, decimal_places=3)
	balance = models.DecimalField( max_digits=10, decimal_places=3, null=True)
	date = models.DateField(auto_now_add=True)
	
	
	def __str__(self):
		return self.label

class Goal(models.Model):

	profile= models.ForeignKey(Profile, default=1, related_name='goals',  on_delete=models.CASCADE)
	label=models.CharField(max_length=120)
	end_date = models.DateField()
	description = models.TextField(null=True, blank=True)
	amount = models.DecimalField( max_digits=10, decimal_places=3)
	balance = models.DecimalField( max_digits=10, decimal_places=3)
	
	
	def __str__(self):
		return self.label

class Deposit(models.Model):
	goal = models.ForeignKey(Goal, default=1, related_name='deposits', on_delete=models.CASCADE)
	amount = models.DecimalField( max_digits=10, decimal_places=3)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return str(self.id)

class Transaction(models.Model):

	user= models.ForeignKey(User, default=1, related_name='transactions',  on_delete=models.CASCADE)
	budget = models.ForeignKey(Budget, default=1, related_name='transactions', on_delete=models.CASCADE)
	amount = models.DecimalField( max_digits=10, decimal_places=3)
	label = models.CharField(max_length=120)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.label

class Expense(models.Model):
	profile= models.ForeignKey(Profile, default=1, related_name='expenses',  on_delete=models.CASCADE)
	label=models.CharField(max_length=120)
	amount = models.DecimalField( max_digits=10, decimal_places=3)
	
	def __str__(self):
		return self.label


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)