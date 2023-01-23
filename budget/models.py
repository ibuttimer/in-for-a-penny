from datetime import datetime, MINYEAR, timezone

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Budget(models.Model):
    """ Model representing a budget """

    TITLE_FIELD = 'title'
    DESCRIPTION_FIELD = 'description'
    START_DATE_FIELD = 'start_date'
    END_DATE_FIELD = 'end_date'
    BASE_CURRENCY_FIELD = 'base_currency'
    USER_FIELD = 'user'

    BUDGET_ATTRIB_TITLE_MAX_LEN: int = 100
    BUDGET_ATTRIB_DESCRIPTION_MAX_LEN: int = 1000
    BUDGET_ATTRIB_CURRENCY_CODE_MAX_LEN: int = 3

    title = models.CharField(
        _('title'), max_length=BUDGET_ATTRIB_TITLE_MAX_LEN, blank=False)

    description = models.CharField(
        _('description'), max_length=BUDGET_ATTRIB_DESCRIPTION_MAX_LEN)

    start_date = models.DateTimeField(
        default=datetime(MINYEAR, 1, 1, tzinfo=timezone.utc))

    end_date = models.DateTimeField(
        default=datetime(MINYEAR, 1, 1, tzinfo=timezone.utc))

    base_currency = models.CharField(
        _('base currency'), max_length=BUDGET_ATTRIB_CURRENCY_CODE_MAX_LEN,
        blank=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BudgetItem(models.Model):
    """ Model representing a budget """

    BUDGET_FIELD = 'budget'
    NAME_FIELD = 'name'
    CURRENCY_FIELD = 'currency'
    AMOUNT_FIELD = 'amount'
    UNITS_FIELD = 'units'

    UNITS_DECIMAL_PLACES = 1

    BUDGET_ITEM_ATTRIB_NAME_MAX_LEN: int = 100
    BUDGET_ITEM_ATTRIB_CURRENCY_CODE_MAX_LEN = \
        Budget.BUDGET_ATTRIB_CURRENCY_CODE_MAX_LEN

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

    name = models.CharField(
        _('name'), max_length=BUDGET_ITEM_ATTRIB_NAME_MAX_LEN, blank=False)

    currency = models.CharField(
        _('base currency'),
        max_length=BUDGET_ITEM_ATTRIB_CURRENCY_CODE_MAX_LEN, blank=False)

    amount = models.DecimalField(
        max_digits=19, decimal_places=6, default=0.0)

    units = models.DecimalField(
        max_digits=19, decimal_places=UNITS_DECIMAL_PLACES, default=1.0)
