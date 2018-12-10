from .models import (Expenses, Budget, Profile)
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
BudgetCreateUpdateSerializer, 
BudgetAmountUpdateSerializer )

# Expenses
from .serializers import (
ExpensesSerializer,
ExpensesCreateUpdateSerializer)

# Profile
from .serializers import (ProfileSerializer)

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
		profile = ProfileDetailViewSerializer(Profile.objects.get(user=request.user))
		return Response(profile.data, status=HTTP_200_OK)

class ExpensesListAPIView(ListAPIView):
	queryset = Expenses.objects.all()
	serializer_class = ExpensesSerializer
	permission_classes = [IsAuthenticated]

	# def get(self, request, format=None):
		# if request.user.is_anonymous:
		#     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		# profile = ProfileDetailViewSerializer(Profile.objects.get(user=request.user))
		# return Response(profile.data, status=HTTP_200_OK)

class ExpensesCreateAPIView(CreateAPIView):
	serializer_class = ExpensesCreateUpdateSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		my_data = request.data
		serializer = self.serializer_class(data=my_data)
		if serializer.is_valid():
			valid_data = serializer.data
			new_data = {
				'budget': Budget.objects.get(id=valid_data['budget']),
				'amount': valid_data['amount'],
				'label': valid_data['label'],
				'date': valid_data['date'],
				'occurances': valid_data['occurances']
			}
			exp=Expenses.objects.create(**new_data)
			return Response(ExpensesSerializer(exp).data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ExpensesCreateUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Expenses.objects.all()
	serializer_class = ExpensesCreateUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'expenses_id'
	permission_classes = [IsAuthenticated]

class BudgetListAPIView(RetrieveAPIView):
	serializer_class = BudgetSerializer
	permission_classes =[IsAuthenticated]

	def get(self, request, format=None):
		if request.user.is_anonymous:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		profile= Profile.objects.get(user=request.user)
		budget =BudgetSerializer(Budget.objects.get(profile=profile))
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

class BudgetAmountUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Budget.objects.all()
	serializer_class = BudgetAmountUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'budget_id'
	permission_classes = [IsAuthenticated]

