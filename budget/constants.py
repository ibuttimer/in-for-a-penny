from pathlib import Path

# name of this app
THIS_APP = Path(__file__).resolve().parent.name


BUDGETS_URL = ""
BUDGET_NEW_URL = "new/"
BUDGET_ITEMS_URL = "item/"
BUDGET_BY_ID_URL = "<int:pk>/"

BUDGETS_ROUTE_NAME = "budgets"
BUDGET_NEW_ROUTE_NAME = "budget_new"
BUDGET_ITEMS_ROUTE_NAME = "budget_items"
BUDGET_BY_ID_ROUTE_NAME = "budget_by_id"


# context related
FORM_CTX = 'form'
SUBMIT_URL_CTX = 'submit_url'
EXPENSES_CTX = 'expenses'
