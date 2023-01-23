import datetime
from http import HTTPStatus
import json

import requests
from decimal import Decimal

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# should be in database
RATES = None
RETRIEVED = None
RATE_BASE = None

# TODO remove dev data
# dev data
RATES = json.loads('{"USD": 1, "AED": 3.67, "AFN": 89.51, "ALL": 107.63, "AMD": 395.83, "ANG": 1.79, "AOA": 509.3, "ARS": 182.64, "AUD": 1.44, "AWG": 1.79, "AZN": 1.7, "BAM": 1.8, "BBD": 2, "BDT": 105.99, "BGN": 1.81, "BHD": 0.376, "BIF": 2060.13, "BMD": 1, "BND": 1.32, "BOB": 6.92, "BRL": 5.19, "BSD": 1, "BTN": 81.12, "BWP": 12.76, "BYN": 2.57, "BZD": 2, "CAD": 1.34, "CDF": 2062.26, "CHF": 0.92, "CLP": 824, "CNY": 6.78, "COP": 4705.18, "CRC": 566.1, "CUP": 24, "CVE": 101.76, "CZK": 22.07, "DJF": 177.72, "DKK": 6.88, "DOP": 56.65, "DZD": 135.95, "EGP": 29.65, "ERN": 15, "ETB": 53.67, "EUR": 0.923, "FJD": 2.17, "FKP": 0.808, "FOK": 6.88, "GBP": 0.808, "GEL": 2.66, "GGP": 0.808, "GHS": 12.55, "GIP": 0.808, "GMD": 63.1, "GNF": 8675.82, "GTQ": 7.85, "GYD": 209.13, "HKD": 7.83, "HNL": 24.67, "HRK": 6.95, "HTG": 148.5, "HUF": 363.79, "IDR": 15076.41, "ILS": 3.4, "IMP": 0.808, "INR": 81.12, "IQD": 1459.52, "IRR": 42082.53, "ISK": 142.58, "JEP": 0.808, "JMD": 153.04, "JOD": 0.709, "JPY": 129.63, "KES": 124.13, "KGS": 85.79, "KHR": 4120.11, "KID": 1.44, "KMF": 454.02, "KRW": 1234.5, "KWD": 0.307, "KYD": 0.833, "KZT": 462.81, "LAK": 16888.37, "LBP": 1507.5, "LKR": 365.25, "LRD": 155.66, "LSL": 17.15, "LYD": 4.77, "MAD": 10.2, "MDL": 18.99, "MGA": 4328.66, "MKD": 56.97, "MMK": 2102.15, "MNT": 3466.43, "MOP": 8.06, "MRU": 36.37, "MUR": 43.94, "MVR": 15.45, "MWK": 1027.52, "MXN": 18.9, "MYR": 4.29, "MZN": 64.25, "NAD": 17.15, "NGN": 453.54, "NIO": 36.51, "NOK": 9.88, "NPR": 129.8, "NZD": 1.55, "OMR": 0.384, "PAB": 1, "PEN": 3.83, "PGK": 3.52, "PHP": 54.43, "PKR": 229.63, "PLN": 4.34, "PYG": 7422.62, "QAR": 3.64, "RON": 4.55, "RSD": 108.35, "RUB": 68.72, "RWF": 1099.74, "SAR": 3.75, "SBD": 8.39, "SCR": 13.6, "SDG": 545.66, "SEK": 10.3, "SGD": 1.32, "SHP": 0.808, "SLE": 19.55, "SLL": 19554.79, "SOS": 568.24, "SRD": 31.87, "SSP": 703.89, "STN": 22.61, "SYP": 2530.78, "SZL": 17.15, "THB": 32.74, "TJS": 10.25, "TMT": 3.5, "TND": 3.09, "TOP": 2.37, "TRY": 18.81, "TTD": 6.76, "TVD": 1.44, "TWD": 30.3, "TZS": 2334.04, "UAH": 36.89, "UGX": 3675.98, "UYU": 39.66, "UZS": 11296.76, "VES": 20.53, "VND": 23456.79, "VUV": 120.57, "WST": 2.66, "XAF": 605.36, "XCD": 2.7, "XDR": 0.74, "XOF": 605.36, "XPF": 110.13, "YER": 250.17, "ZAR": 17.16, "ZMW": 18.59, "ZWL": 745.94}')
RETRIEVED = '2023-01-22'
RATE_BASE = "USD"


def get_rates() -> dict:

    global RATES, RETRIEVED, RATE_BASE

    today = datetime.date.today().strftime("%Y-%m-%d")
    if today != RETRIEVED:
        # free api only updates once a day
        response = requests.get(API_URL)
        if response.status_code == HTTPStatus.OK:
            rate_info = response.json()
            RATES = rate_info['rates']
            RETRIEVED = rate_info['date']
            RATE_BASE = rate_info['base']

    return RATES.copy() if RATES else None


def convert_currency(from_code: str, from_amt: Decimal, to_code: str):

    if from_code in RATES and to_code in RATES:
        result = (Decimal.from_float(RATES[to_code]) /
                  Decimal.from_float(RATES[from_code])) * from_amt
    else:
        result = None
    return result

