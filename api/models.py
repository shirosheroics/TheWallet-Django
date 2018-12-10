
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

	def __str__(self):
		return self.user.username

class Budget(models.Model):
	TYPE_CHOICE = (
		('Food', 'Food'),
		('Health', 'Health'),
		('Emergency', 'Emergency'),
		('Entertainment', 'Entertainment'),
		('Mandatory', 'Mandatory'),
		('Others', 'Others')
	)

	profile= models.ForeignKey(Profile, default=1, related_name='budget',  on_delete=models.CASCADE)
	label=models.CharField(max_length=120)
	category = models.CharField(max_length=13, choices=TYPE_CHOICE)
	amount = models.DecimalField( max_digits=10, decimal_places=3)
	
	def __str__(self):
		return self.category

class Expenses(models.Model):
	OCCURANCE_CHOICE = (
		('None', 'None'),
		('Daily', 'Daily'),
		('Weekly', 'Weekly'),
		('Monthly', 'Monthly'),
		('Annually', 'Annually')
		)

	budget = models.OneToOneField(Budget, on_delete=models.CASCADE)
	amount = models.DecimalField( max_digits=10, decimal_places=3)
	label = models.CharField(max_length=120)
	date = models.DateField(null=True)
	occurances=models.CharField(max_length=8, choices=OCCURANCE_CHOICE)

	def __str__(self):
		return self.label


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)