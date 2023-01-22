from django.forms import DateField, DecimalField
from django.utils.translation import gettext_lazy as _

from django import forms

import ccy

from .models import Budget, BudgetItem


def get_currency_choices():
    choices = [
        ("", "Select One …")
    ]
    choices.extend([
        (code, code) for code in list(ccy.all())
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
