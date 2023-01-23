from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass
from typing import List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View, generic

from .constants import (
    THIS_APP, FORM_CTX, BUDGET_BY_ID_ROUTE_NAME, SUBMIT_URL_CTX,
    BUDGET_NEW_ROUTE_NAME, BUDGETS_ROUTE_NAME, EXPENSES_CTX, BUDGET_ITEM_BY_ID_ROUTE_NAME, BUDGET_ITEM_NEW_ROUTE_NAME,
    TOTAL_CTX
)
from .forms import BudgetForm, BudgetItemForm
from .models import Budget, BudgetItem
from .utils import convert_currency


class BudgetCreate(
    #LoginRequiredMixin,
    View):
    """
    Class-based view for budget creation
    """

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        GET method for Budget
        :param request: http request
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """
        submit_url = reverse(f'{THIS_APP}:{BUDGET_NEW_ROUTE_NAME}')
        return self.render_form(request,
                                self.init_form(BudgetForm()), submit_url)

    @staticmethod
    def init_form(form: BudgetForm):
        """ Initialise form display """
        for field in [Budget.TITLE_FIELD, Budget.DESCRIPTION_FIELD]:
            if field not in form.initial:
                form.initial[field] = ""
        for field in [Budget.START_DATE_FIELD, Budget.END_DATE_FIELD]:
            date = form.initial[field] if field in form.initial else \
                datetime.now()
            form.initial[field] = date.strftime(BudgetForm.DEFAULT_FORMATS[0])
        return form

    @staticmethod
    def render_form(request: HttpRequest, form: BudgetForm,
                    submit_url: str = None,
                    expenses: List[BudgetItemForm] = None,
                    total: Decimal = None) -> HttpResponse:
        return render(request, f'{THIS_APP}/budget_form.html', context={
            FORM_CTX: form,
            SUBMIT_URL_CTX: submit_url,
            EXPENSES_CTX: expenses,
            TOTAL_CTX: total
        })

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        POST method to create Budget
        :param request: http request
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """

        form = BudgetForm(data=request.POST)

        if form.is_valid():
            # save new object
            form.instance.user = request.user

            form.save()
            # django autocommits changes
            # https://docs.djangoproject.com/en/4.1/topics/db/transactions/#autocommit
            success = True
        else:
            success = False

        return redirect(f'{THIS_APP}:{BUDGETS_ROUTE_NAME}') if success else \
            self.render_form(request, form)


class BudgetItemCreate(
    #LoginRequiredMixin,
    View):
    """
    Class-based view for budget item creation
    """

    @staticmethod
    def render_form(request: HttpRequest, form: BudgetForm,
                    submit_url: str = None,
                    expenses: List[BudgetItemForm] = None) -> HttpResponse:
        return render(request, f'{THIS_APP}/budget_form.html', context={
            FORM_CTX: form,
            SUBMIT_URL_CTX: submit_url,
            EXPENSES_CTX: expenses
        })

    def post(self, request: HttpRequest, pk: int, *args, **kwargs) -> HttpResponse:
        """
        POST method to create Budget item
        :param request: http request
        :param pk: id of budget to add to
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """

        budget = get_object_or_404(Budget, id=pk)

        form = BudgetItemForm(data=request.POST)

        if form.is_valid():
            # save new object
            form.instance.budget = budget

            form.save()
            # django autocommits changes
            # https://docs.djangoproject.com/en/4.1/topics/db/transactions/#autocommit
            success = True
        else:
            success = False

        return redirect(BudgetById.url(budget)) if success else \
            self.render_form(request, form)

    @staticmethod
    def init_form(form: BudgetItemForm, budget_item: BudgetItem = None):
        """ Initialise form display """
        for field in [BudgetItem.NAME_FIELD]:
            if field not in form.initial:
                form.initial[field] = ""

        if BudgetItem.AMOUNT_FIELD in form.initial:
            form.initial[BudgetItem.AMOUNT_FIELD] = \
                BudgetItemForm.quantise_amount(budget_item.amount)

        units = budget_item.units \
            if BudgetItem.AMOUNT_FIELD in form.initial and \
               budget_item is not None else BudgetItemForm.DEFAULT_UNITS
        form.initial[BudgetItem.UNITS_FIELD] = \
            BudgetItemForm.quantise_units(units)

        return form


class BudgetList(generic.ListView):
    """
    Class-based view for budget list
    """
    model = Budget
    context_object_name = 'budget_list'


@dataclass
class Expense:
    """ Class representing a budget expense """
    submit_url: str
    form: BudgetItemForm
    total_code: Decimal
    total_base: Decimal


class BudgetById(#LoginRequiredMixin,
        View):
    """
    Class-based view for individual budget view/update
    """
    def get(self, request: HttpRequest,
            pk: int, *args, **kwargs) -> HttpResponse:
        """
        GET method for Budget
        :param request: http request
        :param pk: id of budget to get
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """

        budget = get_object_or_404(Budget, id=pk)

        # perform own budget check
        # own_content_check(request, budget)

        form = BudgetCreate.init_form(
            BudgetForm(instance=budget)
        )

        expenses = []
        for budget_item in list(BudgetItem.objects.filter(**{
            f'{BudgetItem.BUDGET_FIELD}': pk
        })):
            submit_url = BudgetItemById.url(budget_item)

            item_form = BudgetItemCreate.init_form(
                BudgetItemForm(instance=budget_item), budget_item
            )

            raw_amt = budget_item.amount * budget_item.units
            total_code = BudgetItemForm.quantise_amount(raw_amt)
            total_base = BudgetItemForm.quantise_amount(
                convert_currency(
                    budget_item.currency, raw_amt, budget.base_currency)
            )

            expenses.append(
                Expense(submit_url=submit_url, form=item_form,
                        total_code=total_code, total_base=total_base)
            )

        item_form = BudgetItemCreate.init_form(
            BudgetItemForm()
        )

        expenses.append(
            Expense(submit_url= reverse(
                f'{THIS_APP}:{BUDGET_ITEM_NEW_ROUTE_NAME}',
                args=[budget.id]
            ), form=item_form,
            total_code=0, total_base=0)
        )

        return BudgetCreate.render_form(
            request, form, submit_url=self.url(budget), expenses=expenses
        )

    def post(self, request: HttpRequest,
             pk: int, *args, **kwargs) -> HttpResponse:
        """
        POST method to update Budget
        :param request: http request
        :param pk: id of budget to get
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """

        budget = get_object_or_404(Budget, id=pk)

        # perform own budget check
        # own_content_check(request, budget)

        form = BudgetForm(data=request.POST, instance=budget)

        if form.is_valid():
            # update object

            form.save()
            # django autocommits changes
            # https://docs.djangoproject.com/en/4.1/topics/db/transactions/#autocommit
            success = True
        else:
            success = False

        return redirect(f'{THIS_APP}:{BUDGETS_ROUTE_NAME}') if success else \
            BudgetCreate.render_form(request, form, self.url(budget))

    @staticmethod
    def url(budget: Budget) -> str:
        """
        Get url for specified `budget`
        :param budget:
        :return:
        """
        return reverse(
            f'{THIS_APP}:{BUDGET_BY_ID_ROUTE_NAME}', args=[budget.id])


class BudgetItemById(#LoginRequiredMixin,
        View):
    """
    Class-based view for individual budget view/update
    """

    def post(self, request: HttpRequest,
             pk: int, *args, **kwargs) -> HttpResponse:
        """
        POST method to update BudgetItem
        :param request: http request
        :param pk: id of budget item to update
        :param args: additional arbitrary arguments
        :param kwargs: additional keyword arguments
        :return: http response
        """

        budget_item = get_object_or_404(BudgetItem, id=pk)

        # perform own budget check
        # own_content_check(request, budget)

        form = BudgetItemForm(data=request.POST, instance=budget_item)

        if form.is_valid():
            # update object

            form.save()
            # django autocommits changes
            # https://docs.djangoproject.com/en/4.1/topics/db/transactions/#autocommit
            success = True
        else:
            success = False

        return redirect(f'{THIS_APP}:{BUDGETS_ROUTE_NAME}') if success else \
            BudgetCreate.render_form(request, form, BudgetById.url(pk))

    @staticmethod
    def url(budget_item: BudgetItem) -> str:
        """
        Get url for specified `budget`
        :param budget_item:
        :return:
        """
        return reverse(
            f'{THIS_APP}:{BUDGET_ITEM_BY_ID_ROUTE_NAME}', args=[budget_item.id])


def own_content_check(
        request: HttpRequest, budget: Budget,
        raise_ex: bool = True) -> bool:
    """
    Check request user is budget owner
    :param request: http request
    :param budget: budget
    :param raise_ex: raise exception if not own; default True
    """
    is_own = request.user.id == budget.user.id
    if not is_own and raise_ex:
        raise PermissionDenied(
            "Budgets may only be accessed by their owners")
    return is_own
