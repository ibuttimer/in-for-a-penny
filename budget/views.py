from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View, generic

from in_for_a_penny.constants import HOME_ROUTE_NAME
from .constants import (
    THIS_APP, FORM_CTX, BUDGET_BY_ID_ROUTE_NAME, SUBMIT_URL_CTX,
    BUDGET_NEW_ROUTE_NAME, BUDGETS_ROUTE_NAME
)
from .forms import BudgetForm
from .models import Budget


class BudgetCreate(LoginRequiredMixin, View):
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
                    submit_url: str = None) -> HttpResponse:
        return render(request, f'{THIS_APP}/budget_form.html', context={
            FORM_CTX: form,
            SUBMIT_URL_CTX: submit_url
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


class BudgetList(generic.ListView):
    """
    Class-based view for budget list
    """
    model = Budget
    context_object_name = 'budget_list'


class BudgetById(LoginRequiredMixin, View):
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
        own_content_check(request, budget)

        return BudgetCreate.render_form(
            request, BudgetForm(instance=budget), self.url(budget))

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
        own_content_check(request, budget)

        form = BudgetForm(data=request.POST, instance=budget)

        if form.is_valid():
            # update object

            form.save()
            # django autocommits changes
            # https://docs.djangoproject.com/en/4.1/topics/db/transactions/#autocommit
            success = True
        else:
            success = False

        return redirect(HOME_ROUTE_NAME) if success else \
            BudgetCreate.render_form(request, form, self.url(budget))

    def url(self, budget: Budget) -> str:
        """
        Get url for specified `budget`
        :param budget:
        :return:
        """
        return reverse(
            f'{THIS_APP}:{BUDGET_BY_ID_ROUTE_NAME}', args=[budget.id])


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
