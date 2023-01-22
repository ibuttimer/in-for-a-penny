from django.contrib import admin

from budget.models import Budget, BudgetItem


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """ Class representing the Budget model in the admin interface """
    list_display = (
        Budget.TITLE_FIELD,
        Budget.START_DATE_FIELD,
        Budget.BASE_CURRENCY_FIELD,
    )


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    """ Class representing the BudgetItem model in the admin interface """
    list_display = (
        BudgetItem.NAME_FIELD,
        BudgetItem.UNITS_FIELD,
        BudgetItem.CURRENCY_FIELD,
    )
