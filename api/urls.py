from django.urls import path
from .views import UserCreateAPIView
from rest_framework_jwt.views import obtain_jwt_token

#User Imports
from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    ProfileDetailAPIView,
    ProfileUpdateAPIView
)

#Budget Imports
from .views import(
    BudgetListAPIView,
    BudgetCreateAPIView,
    BudgetCreateUpdateAPIView
)

#Expense Imports
from .views import(
    ExpenseListAPIView,
    ExpenseCreateAPIView,
    ExpenseCreateUpdateAPIView
)

#Transaction
from .views import(
    TransactionListAPIView,
    TransactionCreateAPIView,
    TransactionCreateUpdateAPIView
)

urlpatterns = [
    # User's
    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('profile/', ProfileDetailAPIView.as_view(), name='api-profile-detail'),
    path('profile/update/', ProfileUpdateAPIView.as_view(), name='api-profile-update'),
	# path('profile/<int:user_id>/update', ProfileUpdateAPIView.as_view(), name='api-profile-update'),
    #Budget
    path('budget/list/', BudgetListAPIView.as_view(), name='api-budget-list'),
    path('budget/create/', BudgetCreateAPIView.as_view(), name='api-budget-create'),
	path('budget/<int:budget_id>/update/', BudgetCreateUpdateAPIView.as_view(), name='api-budget-update'),
    #Transaction
    path('transaction/list/', TransactionListAPIView.as_view(), name='api-transaction-list'),
    path('transaction/create/', TransactionCreateAPIView.as_view(), name='api-transaction-create'),
	path('transaction/<int:transaction_id>/update/', TransactionCreateUpdateAPIView.as_view(), name='api-transaction-update'),
    #Expense
    path('expense/list/', ExpenseListAPIView.as_view(), name='api-expense-list'),
    path('expense/create/', ExpenseCreateAPIView.as_view(), name='api-expense-create'),
	path('expense/<int:budget_id>/update/', ExpenseCreateUpdateAPIView.as_view(), name='api-expense-update'),
]