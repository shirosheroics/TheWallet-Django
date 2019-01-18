from .models import (Expense, Transaction, Budget, Profile, Goal, Deposit)
from django.contrib.auth.models import User
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
)
from .serializers import (UserCreateSerializer, UserLoginSerializer)

# Budget
from .serializers import (
BudgetSerializer, 
BudgetCreateUpdateSerializer )

# Goal
from .serializers import (
GoalSerializer, 
GoalCreateUpdateSerializer )

# Expense
from .serializers import (
ExpenseSerializer, 
ExpenseCreateUpdateSerializer )

# Transaction
from .serializers import (
TransactionSerializer,
TransactionCreateUpdateSerializer)

# Deposit
from .serializers import (
DepositSerializer,
DepositCreateUpdateSerializer)

# Profile
from .serializers import (ProfileSerializer, ProfileCreateUpdateSerializer)

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer

class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer
	permission_classes = [AllowAny,]
	def post(self, request):
		my_data = request.data
		serializer = UserLoginSerializer(data=my_data)
		if serializer.is_valid(raise_exception=True):
			valid_data = serializer.data
			return Response(valid_data, status=HTTP_200_OK)
		return Response(serializer.errors, HTTP_400_BAD_REQUEST)

class ProfileDetailAPIView(RetrieveAPIView):
	serializer_class = ProfileSerializer
	permission_classes =[IsAuthenticated]
	
	def get(self, request, format=None):
		if request.user.is_anonymous:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		profile = ProfileSerializer(Profile.objects.get(user=request.user))
		return Response(profile.data, status=HTTP_200_OK)

class ProfileUpdateAPIView(RetrieveUpdateAPIView):
	serializer_class = ProfileCreateUpdateSerializer
	permission_classes =[IsAuthenticated]

	def get(self, request, format=None):
		if request.user.is_anonymous:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		profile = ProfileSerializer(Profile.objects.get(user=request.user))
		return Response(profile.data, status=HTTP_200_OK)
	
	def put(self, request, format=None):
		if request.user.is_anonymous:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		my_data = request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			# new_data = {
			# 	'phoneNo': valid_data['phoneNo'],
			# 	'dob': valid_data['dob'],
			# 	'gender': valid_data['gender'],
			# 	'income': valid_data['income']
			# }
			profile=Profile.objects.get(user=request.user)
			profile.phoneNo = valid_data['phoneNo']
			profile.dob = valid_data['dob']
			profile.gender = valid_data['gender']
			profile.income = valid_data['income']
			profile.balance = valid_data['balance']
			profile.savings = valid_data['savings']
			profile.automated = valid_data['automated']
			profile.latitude = valid_data['latitude']
			profile.longitude = valid_data['longitude']
			profile.accuracy = valid_data['accuracy']
			profile.save()
			return Response(ProfileSerializer(profile).data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# Transaction

class TransactionListAPIView(ListAPIView):
	queryset = Transaction.objects.all()
	serializer_class = TransactionSerializer
	permission_classes = [IsAuthenticated]

	# def get(self, request, format=None):
		# if request.user.is_anonymous:
		#     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		# profile = ProfileDetailViewSerializer(Profile.objects.get(user=request.user))
		# return Response(profile.data, status=HTTP_200_OK)

class TransactionCreateAPIView(CreateAPIView):
	serializer_class = TransactionCreateUpdateSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		my_data = request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			new_data = {
				'user': User.objects.get(id=request.user.id),
				'budget': Budget.objects.get(id=valid_data['budget']),
				'amount': valid_data['amount'],
				'label': valid_data['label']
			}
			trans=Transaction.objects.create(**new_data)
			budget= Budget.objects.get(id=trans.budget.id)
			budget.balance = float(budget.balance)-float(trans.amount)
			budget.save()
			return Response(TransactionSerializer(trans).data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class TransactionCreateUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Transaction.objects.all()
	serializer_class = TransactionCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'transaction_id'
	permission_classes = [IsAuthenticated]

	def put(self, request, transaction_id):
		my_data = request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			transaction = Transaction.objects.get(id=transaction_id)
			budget= Budget.objects.get(id=valid_data['budget'])
			budget.balance = float(budget.balance)+(float(transaction.amount)-float(valid_data['amount']))
			transaction.amount = valid_data['amount']
			transaction.label = valid_data['label']
			transaction.save()
			budget.save()
			return Response(TransactionSerializer(transaction).data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class TransactionDeleteView(DestroyAPIView):
	queryset = Transaction.objects.all()
	serializer_class = TransactionSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'transaction_id'
	permission_classes = [IsAuthenticated]

	def delete(self, request, transaction_id):
		my_data = request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			budget= Budget.objects.get(id=valid_data['budget'])
			budget.balance = float(budget.balance)+float(valid_data['amount'])
			budget.save()
			transaction = Transaction.objects.get(id=transaction_id)
			transaction.delete()
			return Response((transaction_id), status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#Budgets

class BudgetListAPIView(RetrieveAPIView):
	serializer_class = BudgetSerializer
	permission_classes =[IsAuthenticated]

	def get(self, request, format=None):
		if request.user.is_anonymous:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		profile= Profile.objects.get(user=request.user)
		budget =BudgetSerializer(Budget.objects.filter(profile=profile), many=True)
		return Response(budget.data, status=HTTP_200_OK)

class BudgetCreateAPIView(CreateAPIView):
	serializer_class = BudgetCreateUpdateSerializer
	permission_classes =[IsAuthenticated]

	def post(self, request):
		tempBud=[]
		for my_data in request.data:
			serializer = self.serializer_class(data=my_data)
			if serializer.is_valid():
				valid_data = serializer.data
				new_data = {
					'category': valid_data['category'],
					'amount': valid_data['amount'],
					'profile': Profile.objects.get(user=request.user.id),
					'label': valid_data['label'],
					'balance': valid_data['amount']
				}
				bud = Budget.objects.create(**new_data)
				tempBud.append(BudgetSerializer(bud).data)
			else:
				return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		return Response(tempBud, status=HTTP_200_OK)
		

class BudgetCreateUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Budget.objects.all()
	serializer_class = BudgetCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'budget_id'
	permission_classes = [IsAuthenticated]


class BudgetDeleteAPIView(DestroyAPIView):
	queryset = Budget.objects.all()
	serializer_class = BudgetCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'budget_id'
	permission_classes = [IsAuthenticated]


#Goal

class GoalListAPIView(RetrieveAPIView):
	serializer_class = GoalSerializer
	permission_classes =[IsAuthenticated]

	def get(self, request, format=None):
		if request.user.is_anonymous:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		profile= Profile.objects.get(user=request.user)
		goal =GoalSerializer(Goal.objects.filter(profile=profile), many=True)
		return Response(goal.data, status=HTTP_200_OK)

class GoalCreateAPIView(CreateAPIView):
	serializer_class = GoalCreateUpdateSerializer
	permission_classes =[IsAuthenticated]

	def post(self, request):
		tempGoal=[]
		print(request.data)
		for my_data in request.data:
			serializer = self.serializer_class(data=my_data)
			if serializer.is_valid():
				valid_data = serializer.data
				# print(valid_data)
				new_data = {
					'end_date': valid_data['end_date'],
					'amount': valid_data['amount'],
					'profile': Profile.objects.get(user=request.user.id),
					'label': valid_data['label'],
					'balance': valid_data['amount'],
					'description': valid_data['description']
					
				}
				goal = Goal.objects.create(**new_data)
				tempGoal.append(GoalSerializer(goal).data)
			else :
				return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		return Response(tempGoal, status=HTTP_200_OK)

class GoalCreateUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Goal.objects.all()
	serializer_class = GoalCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'goal_id'
	permission_classes = [IsAuthenticated]

class GoalDeleteAPIView(DestroyAPIView):
	queryset = Goal.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'goal_id'
	permission_classes = [IsAuthenticated]

	def delete(self, request,goal_id):
		my_data = request.data
		if "id" in my_data :
			goal= Goal.objects.get(id=my_data['id'])
			total_deposits=float(goal.amount)-float(goal.balance)
			profile=Profile.objects.get(user=request.user)
			profile.savings = float(profile.savings)+float(total_deposits)			
			profile.save()
			goal.delete()
			return Response((goal_id), status=HTTP_200_OK)
		return Response("Goal id not found", status=HTTP_400_BAD_REQUEST)

#Expense

class ExpenseListAPIView(RetrieveAPIView):
	serializer_class = ExpenseSerializer
	permission_classes =[IsAuthenticated]

	def get(self, request, format=None):
		if request.user.is_anonymous:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		profile= Profile.objects.get(user=request.user)
		expenses =ExpenseSerializer(Expense.objects.filter(profile=profile.id),many=True)
		return Response(expenses.data, status=HTTP_200_OK)

class ExpenseCreateAPIView(CreateAPIView):
	serializer_class = ExpenseCreateUpdateSerializer
	permission_classes =[IsAuthenticated]

	def post(self, request):
		tempExp=[]
		for my_data in request.data:
			serializer = self.serializer_class(data=my_data)
			if serializer.is_valid():
				valid_data = serializer.data
				new_data = {
					'amount': valid_data['amount'],
					'profile': Profile.objects.get(user=request.user.id),
					'label': valid_data['label'],
				}
				exp = Expense.objects.create(**new_data)
				profile = Profile.objects.get(user=request.user)
				profile.balance= float(profile.balance) - float(exp.amount)
				profile.save()
				tempExp.append(ExpenseSerializer(exp).data)
			else:
				return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		return Response(tempExp, status=HTTP_200_OK)
		

class ExpenseCreateUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Expense.objects.all()
	serializer_class = ExpenseCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'expense_id'
	permission_classes = [IsAuthenticated]

	def put(self, request,expense_id):
		my_data= request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			# new_data = {
			# 	'amount': valid_data['amount'],
			# 	'profile': Profile.objects.get(user=request.user.id),
			# 	'label': valid_data['label'],
			# }
			exp = Expense.objects.get(id=expense_id)
			old_amount=exp.amount
			exp.amount=valid_data['amount'] 
			exp.label=valid_data['label'] 
			profile = Profile.objects.get(user=request.user)
			profile.balance= float(profile.balance) + (float(old_amount)-float(valid_data['amount'] ))
			profile.save()
			exp.save()
			return Response(ExpenseCreateUpdateSerializer(exp).data, status=HTTP_200_OK)
		else:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ExpenseDeleteAPIView(DestroyAPIView):
	queryset = Expense.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'expense_id'
	permission_classes = [IsAuthenticated]

	def delete(self, request,expense_id):
		my_data = request.data
		if "id" in my_data :
			expense= Expense.objects.get(id=my_data['id'])
			profile=Profile.objects.get(user=request.user)
			profile.balance = float(profile.balance)+float(expense.amount)			
			profile.save()
			expense.delete()
			return Response((expense_id), status=HTTP_200_OK)
		return Response("Expense id not found", status=HTTP_400_BAD_REQUEST)


# Deposits 

class DepositListAPIView(ListAPIView):
	queryset = Deposit.objects.all()
	serializer_class = DepositSerializer
	permission_classes = [IsAuthenticated]

	# def get(self, request, format=None):
	# 	if request.user.is_anonymous:
	# 	    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
	# 	goal= Goal.objects.get(id = )
	# 	Deposit = DepositSerializer(Deposit.objects.get(goal=Goal.objects.get(id =  )request.user))
	# 	return Response(profile.data, status=HTTP_200_OK)

class DepositCreateAPIView(CreateAPIView):
	serializer_class = DepositCreateUpdateSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		my_data = request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			new_data = {
				'goal': Goal.objects.get(id=valid_data['goal']),
				'amount': valid_data['amount']
			}
			dep=Deposit.objects.create(**new_data)
			goal=Goal.objects.get(id=dep.goal.id)
			goal.balance= float(goal.balance)-float(dep.amount)
			goal.save()
			profile=Profile.objects.get(user=request.user)
			profile.savings = float(profile.savings)-float(dep.amount)			
			profile.save()
			return Response(DepositSerializer(dep).data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class DepositCreateUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Deposit.objects.all()
	serializer_class = DepositCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'deposit_id'
	permission_classes = [IsAuthenticated]

	def put(self, request, deposit_id):
		my_data = request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			deposit = Deposit.objects.get(id=deposit_id)
			goal= Goal.objects.get(id=valid_data['goal'])
			goal.balance = float(goal.balance)+(float(deposit.amount)-float(valid_data['amount']))
			deposit.amount = valid_data['amount']
			deposit.save()
			goal.save()
			return Response(DepositCreateUpdateSerializer(deposit).data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class DepositDeleteView(DestroyAPIView):
	queryset =Deposit.objects.all()
	serializer_class =DepositSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'deposit_id'
	permission_classes = [IsAuthenticated]

	def delete(self, request,deposit_id):
		my_data = request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			deposit =Deposit.objects.get(id=deposit_id)
			goal= Goal.objects.get(id=valid_data['goal'])
			goal.balance = float(goal.balance)+float(valid_data['amount'])
			goal.save()
			profile=Profile.objects.get(user=request.user)
			profile.savings = float(profile.savings)+float(deposit.amount)			
			profile.save()
			deposit.delete()
			return Response((deposit_id), status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
