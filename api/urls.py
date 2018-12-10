from django.urls import path
from .views import UserCreateAPIView
from rest_framework_jwt.views import obtain_jwt_token

#User Imports
from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    ProfileDetailAPIView
)

#Budget Imports
from .views import(
    BudgetListAPIView,
    BudgetCreateAPIView,
    BudgetCreateUpdateAPIView,
    BudgetAmountUpdateAPIView
)

#Expenses
from .views import(
    ExpensesListAPIView,
    ExpensesCreateAPIView,
    ExpensesCreateUpdateAPIView
)

urlpatterns = [
    # User's
    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('profile/', ProfileDetailAPIView.as_view(), name='api-profile-detail'),
	# path('profile/<int:user_id>/update', ProfileUpdateAPIView.as_view(), name='api-profile-update'),
    #Budget
    path('budget/list/', BudgetListAPIView.as_view(), name='api-budget-list'),
    path('budget/create/', BudgetCreateAPIView.as_view(), name='api-budget-create'),
	path('budget/<int:budget_id>/update/', BudgetCreateUpdateAPIView.as_view(), name='api-budget-update'),
	path('budget/<int:budget_id>/amount-update/', BudgetAmountUpdateAPIView.as_view(), name='api-budget-amount-update'),
    #Expenses
    path('expenses/list/', ExpensesListAPIView.as_view(), name='api-expenses-list'),
    path('expenses/create/', ExpensesCreateAPIView.as_view(), name='api-expenses-create'),
	path('expenses/<int:expenses_id>/update/', ExpensesCreateUpdateAPIView.as_view(), name='api-expenses-update'),
]