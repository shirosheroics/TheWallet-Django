from .models import (Expenses, Budget, Profile)
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
)
from .serializers import UserCreateSerializer
# Budget
from .serializers import 
(BudgetSerializer, 
BudgetCreateUpdateSerializer, 
BudgetAmountUpdateSerializer )

# Expenses
from .serializer import 
ExpensesSerializer,
ExpensesCreateUpdateSerializer)

# Profile
from .serializer import 
(ProfileSerializer)

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
	serializer_class = ProfileDetailViewSerializer
	permission_classes =[IsAuthenticated,IsUser]
	
	def get(self, request, format=None):
		if request.user.is_anonymous:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		profile = ProfileDetailViewSerializer(Profile.objects.get(user=request.user))
		return Response(profile.data, status=HTTP_200_OK)
