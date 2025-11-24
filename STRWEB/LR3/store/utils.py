import requests
from django.conf import settings

NBRB_RATES_URL = "https://www.nbrb.by/api/exrates/rates?periodicity=0"
EXCHANGE_API_URL = "https://api.exchangerate.host/latest"


def fetch_nbrb_rates(symbols=None):
    """
    Курсы к BYN из API Национального банка РБ.
    symbols: список строк-код валют, например ["USD","EUR","RUB"]; None — все.
    Возвращает: {'USD': 2.50, 'EUR': 2.70, …}
    """
    resp = requests.get(NBRB_RATES_URL, timeout=5)
    resp.raise_for_status()
    data = resp.json()  # список записей
    rates = {}
    for entry in data:
        code  = entry["Cur_Abbreviation"]    # например "USD"
        scale = entry["Cur_Scale"]           # например 1, 10, 100
        rate  = entry["Cur_OfficialRate"]    # курс за scale единиц
        if symbols is None or code in symbols:
            rates[code] = rate / scale
    return rates


def fetch_exchange_rates(base="BYN", symbols=None):
    """
    Курсы от exchangerate.host.
    base: базовая валюта (по умолчанию "BYN").
    symbols: список нужных валют, например ["USD","EUR","RUB"].
    Возвращает: {'USD': 0.39, 'EUR': 0.35, …}
    """
    params = {"base": base}
    if symbols:
        params["symbols"] = ",".join(symbols)
    resp = requests.get(EXCHANGE_API_URL, params=params, timeout=5)
    if not resp.ok:
        return {}
    return resp.json().get("rates", {})


# def fetch_news(query="животные OR питомцы OR зоотовары OR зоопарк",
#                page=1, page_size=5):
#     """
#     Новости через newsapi.org.
#     query: поисковая строка,
#     page: номер страницы,
#     page_size: сколько взять за раз.
#     """
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q":        query,
#         "apiKey":   settings.NEWS_API_KEY,
#         "page":     page,
#         "pageSize": page_size,
#         "language": "ru",
#         "sortBy":   "publishedAt",
#     }
#     resp = requests.get(url, params=params, timeout=5)
#     if not resp.ok:
#         return []
#     return resp.json().get("articles", [])
