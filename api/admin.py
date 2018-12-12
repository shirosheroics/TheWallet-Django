from django.contrib import admin
from .models import (Profile, Budget, Expense, Transaction)

admin.site.register(Profile)
admin.site.register(Budget)
admin.site.register(Transaction)
admin.site.register(Expense)


