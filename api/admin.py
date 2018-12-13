from django.contrib import admin
from .models import (Profile, Budget, Expense, Transaction, Deposit, Goal)

admin.site.register(Profile)
admin.site.register(Budget)
admin.site.register(Transaction)
admin.site.register(Expense)
admin.site.register(Deposit)
admin.site.register(Goal)


