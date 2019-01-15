from django.urls import path
from .views import UserCreateAPIView
from rest_framework_jwt.views import obtain_jwt_token

# User Imports
from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    ProfileDetailAPIView,
    ProfileUpdateAPIView,
)

# Budget Imports
from .views import (
    BudgetListAPIView,
    BudgetCreateAPIView,
    BudgetCreateUpdateAPIView,
    BudgetDeleteAPIView,
)

# Goal Imports
from .views import (
    GoalListAPIView,
    GoalCreateAPIView,
    GoalCreateUpdateAPIView,
    GoalDeleteAPIView,
)

# Expense Imports
from .views import (
    ExpenseListAPIView,
    ExpenseCreateAPIView,
    ExpenseCreateUpdateAPIView,
    ExpenseDeleteAPIView,
)

# Transaction
from .views import (
    TransactionListAPIView,
    TransactionCreateAPIView,
    TransactionCreateUpdateAPIView,
    TransactionDeleteView,
)

# Deposit
from .views import (
    DepositListAPIView,
    DepositCreateAPIView,
    DepositCreateUpdateAPIView,
    DepositDeleteView,
)


urlpatterns = [
    # User's
    path("login/", obtain_jwt_token, name="login"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("profile/", ProfileDetailAPIView.as_view(), name="api-profile-detail"),
    path("profile/update/", ProfileUpdateAPIView.as_view(), name="api-profile-update"),
    # path('profile/<int:user_id>/update', ProfileUpdateAPIView.as_view(), name='api-profile-update'),
    # Budget
    path("budget/list/", BudgetListAPIView.as_view(), name="api-budget-list"),
    path("budget/create/", BudgetCreateAPIView.as_view(), name="api-budget-create"),
    path(
        "budget/<int:budget_id>/update/",
        BudgetCreateUpdateAPIView.as_view(),
        name="api-budget-update",
    ),
    path(
        "budget/<int:budget_id>/delete/",
        BudgetDeleteAPIView.as_view(),
        name="api-budget-delete",
    ),
    # Goal
    path("goal/list/", GoalListAPIView.as_view(), name="api-goal-list"),
    path("goal/create/", GoalCreateAPIView.as_view(), name="api-goal-create"),
    path(
        "goal/<int:goal_id>/update/",
        GoalCreateUpdateAPIView.as_view(),
        name="api-goal-update",
    ),
    path(
        "goal/<int:goal_id>/delete/",
        GoalDeleteAPIView.as_view(),
        name="api-goal-delete",
    ),
    # Transaction
    path(
        "transaction/list/",
        TransactionListAPIView.as_view(),
        name="api-transaction-list",
    ),
    path(
        "transaction/create/",
        TransactionCreateAPIView.as_view(),
        name="api-transaction-create",
    ),
    path(
        "transaction/<int:transaction_id>/update/",
        TransactionCreateUpdateAPIView.as_view(),
        name="api-transaction-update",
    ),
    path(
        "transaction/<int:transaction_id>/delete/",
        TransactionDeleteView.as_view(),
        name="api-transaction-delete",
    ),
    # Deposit
    path("deposit/list/", DepositListAPIView.as_view(), name="api-deposit-list"),
    path("deposit/create/", DepositCreateAPIView.as_view(), name="api-deposit-create"),
    path(
        "deposit/<int:deposit_id>/update/",
        DepositCreateUpdateAPIView.as_view(),
        name="api-deposit-update",
    ),
    path(
        "deposit/<int:deposit_id>/delete/",
        DepositDeleteView.as_view(),
        name="api-deposit-delete",
    ),
    # Expense
    path("expense/list/", ExpenseListAPIView.as_view(), name="api-expense-list"),
    path("expense/create/", ExpenseCreateAPIView.as_view(), name="api-expense-create"),
    path(
        "expense/<int:expense_id>/update/",
        ExpenseCreateUpdateAPIView.as_view(),
        name="api-expense-update",
    ),
    path(
        "expense/<int:expense_id>/delete/",
        ExpenseDeleteAPIView.as_view(),
        name="api-expense-delete",
    ),
]
