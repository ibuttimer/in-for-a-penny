from django.forms import DateField, DecimalField
from django.utils.translation import gettext_lazy as _

from django import forms

from .models import Budget, BudgetItem


class BudgetForm(forms.ModelForm):
    """
    Form to create/update a budget.
    """

    title = forms.CharField(
        label=_("Title"),
        max_length=Budget.BUDGET_ATTRIB_TITLE_MAX_LEN,
        required=True)

    description = forms.CharField(
        label=_("Description"),
        max_length=Budget.BUDGET_ATTRIB_DESCRIPTION_MAX_LEN,
        required=False)

    start_date = DateField(input_formats=['%d/%m/%Y'])

    end_date = DateField(input_formats=['%d/%m/%Y'])

    base_currency = forms.CharField(
        label=_("Base currency"),
        max_length=Budget.BUDGET_ATTRIB_CURRENCY_CODE_MAX_LEN,
        required=True)

    class Meta:
        model = Budget
        fields = [
            Budget.TITLE_FIELD, Budget.DESCRIPTION_FIELD,
            Budget.START_DATE_FIELD, Budget.END_DATE_FIELD,
            Budget.BASE_CURRENCY_FIELD
        ]


class BudgetItemForm(forms.ModelForm):
    """
    Form to create/update a budget item.
    """

    name = forms.CharField(
        label=_("Name"),
        max_length=BudgetItem.BUDGET_ITEM_ATTRIB_NAME_MAX_LEN,
        required=True)

    currency = forms.CharField(
        label=_("Currency"),
        max_length=BudgetItem.BUDGET_ITEM_ATTRIB_CURRENCY_CODE_MAX_LEN,
        required=True)

    amount = DecimalField(decimal_places=2)

    units = DecimalField(decimal_places=1)
