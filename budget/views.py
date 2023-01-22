from decimal import Decimal
from dataclasses import dataclass
from typing import List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View, generic

from in_for_a_penny.constants import HOME_ROUTE_NAME, BASE_APP_NAME
from .constants import (
    THIS_APP, FORM_CTX, BUDGET_BY_ID_ROUTE_NAME, SUBMIT_URL_CTX,
    BUDGET_NEW_ROUTE_NAME, BUDGETS_ROUTE_NAME, EXPENSES_CTX, BUDGET_ITEM_BY_ID_ROUTE_NAME, BUDGET_ITEM_NEW_ROUTE_NAME
)
from .forms import BudgetForm, BudgetItemForm
from .models import Budget, BudgetItem


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
        return self.render_form(request, BudgetForm(), submit_url)

    @staticmethod
    def render_form(request: HttpRequest, form: BudgetForm,
                    submit_url: str = None,
                    expenses: List[BudgetItemForm] = None) -> HttpResponse:
        return render(request, f'{THIS_APP}/budget_form.html', context={
            FORM_CTX: form,
            SUBMIT_URL_CTX: submit_url,
            EXPENSES_CTX: expenses
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

        # submit_url = reverse(f'{THIS_APP}:{BUDGET_NEW_ROUTE_NAME}')

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

        form = BudgetForm(instance=budget)
        for field in [
            Budget.START_DATE_FIELD, Budget.END_DATE_FIELD
        ]:
            form.initial[field] = \
                budget.start_date.strftime(BudgetForm.DEFAULT_FORMATS[0])

        expenses = []
        for budget_item in list(BudgetItem.objects.filter(**{
            f'{BudgetItem.BUDGET_FIELD}': pk
        })):
            submit_url = BudgetItemById.url(budget_item)
            item_form = BudgetItemForm(instance=budget_item)
            item_form.initial[BudgetItem.AMOUNT_FIELD] = \
                budget_item.amount.quantize(BudgetItemForm.AMOUNT_EXP)
            item_form.initial[BudgetItem.UNITS_FIELD] = \
                budget_item.units.quantize(BudgetItemForm.UNITS_EXP)

            expenses.append(
                Expense(submit_url=submit_url, form=item_form)
            )

        item_form = BudgetItemForm()
        item_form.initial[BudgetItem.UNITS_FIELD] = \
            BudgetItemForm.DEFAULT_UNITS

        expenses.append(
            Expense(submit_url= reverse(
                f'{THIS_APP}:{BUDGET_ITEM_NEW_ROUTE_NAME}',
                args=[budget.id]
            ), form=item_form)
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
