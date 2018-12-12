from .models import (Expense, Transaction, Budget, Profile)
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

# Expense
from .serializers import (
ExpenseSerializer, 
ExpenseCreateUpdateSerializer )

# Transaction
from .serializers import (
TransactionSerializer,
TransactionCreateUpdateSerializer)

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
			profile.save()
			return Response(ProfileSerializer(profile).data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

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
			return Response(TransactionSerializer(trans).data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class TransactionCreateUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Transaction.objects.all()
	serializer_class = TransactionCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'transaction_id'
	permission_classes = [IsAuthenticated]

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
		my_data = request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			new_data = {
				'category': valid_data['category'],
				'amount': valid_data['amount'],
				'profile': Profile.objects.get(user=request.user.id),
				'label': valid_data['label'],
			}
			bud = Budget.objects.create(**new_data)
			return Response(BudgetSerializer(bud).data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class BudgetCreateUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Budget.objects.all()
	serializer_class = BudgetCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'budget_id'
	permission_classes = [IsAuthenticated]


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
		my_data = request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			new_data = {
				'amount': valid_data['amount'],
				'profile': Profile.objects.get(user=request.user.id),
				'label': valid_data['label'],
			}
			exp = Expense.objects.create(**new_data)
			return Response(ExpenseSerializer(exp).data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ExpenseCreateUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Expense.objects.all()
	serializer_class = ExpenseCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'expense_id'
	permission_classes = [IsAuthenticated]


