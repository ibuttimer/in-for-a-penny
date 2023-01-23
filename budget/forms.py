from decimal import Decimal
from django.forms import DateField, DecimalField
from django.utils.translation import gettext_lazy as _

from django import forms

import ccy

from .models import Budget, BudgetItem


def get_currency_choices():
    choices = [
        ("", "Choose")
    ]
    choices.extend([
        (code, code) for code in list(
            map(lambda code: code.upper(), ccy.all())
        )
    ])
    return choices


class BudgetForm(forms.ModelForm):
    """
    Form to create/update a budget.
    """

    DEFAULT_FORMATS = [
        '%d-%m-%Y',  # '25-10-2006'
        '%d/%m/%Y',  # '25/10/2006'
        '%d %m %Y',  # '25 10 2006'
        '%d-%m-%y',  # '25-10-06'
        '%d/%m/%y',  # '25/10/06'
        '%d %m %y',  # '25 10 06'
    ]
    CURRENCY_CHOICES = get_currency_choices()

    title = forms.CharField(
        label=_("Title"),
        max_length=Budget.BUDGET_ATTRIB_TITLE_MAX_LEN,
        required=True)

    description = forms.CharField(
        label=_("Description"),
        max_length=Budget.BUDGET_ATTRIB_DESCRIPTION_MAX_LEN,
        required=False)

    start_date = DateField(input_formats=DEFAULT_FORMATS)

    end_date = DateField(input_formats=DEFAULT_FORMATS)

    base_currency = forms.ChoiceField(
        label=_("Base currency"),
        required=True,
        choices = CURRENCY_CHOICES
    )

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

    # e.g. Decimal(10) ** -2       # same as Decimal('0.01')
    AMOUNT_EXP = Decimal(10) ** -2
    UNITS_EXP = Decimal(10) ** -BudgetItem.UNITS_DECIMAL_PLACES

    DEFAULT_UNITS = Decimal('1').quantize(UNITS_EXP)

    name = forms.CharField(
        label=_("Name"),
        max_length=BudgetItem.BUDGET_ITEM_ATTRIB_NAME_MAX_LEN,
        required=True)

    currency = forms.ChoiceField(
        label=_("Currency"),
        required=True,
        choices = BudgetForm.CURRENCY_CHOICES
    )

    amount = DecimalField(decimal_places=2)

    units = DecimalField(decimal_places=1)

    class Meta:
        model = BudgetItem
        fields = [
            BudgetItem.NAME_FIELD, BudgetItem.CURRENCY_FIELD,
            BudgetItem.AMOUNT_FIELD, BudgetItem.UNITS_FIELD
        ]

    @staticmethod
    def quantise_amount(amount: Decimal):
        return amount.quantize(BudgetItemForm.AMOUNT_EXP)

    @staticmethod
    def quantise_units(units: Decimal):
        return units.quantize(BudgetItemForm.UNITS_EXP)
