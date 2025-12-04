from tools.finance_core import get_financials

def get_financial_data(stock_name: str) -> str:
    msg, _ = get_financials(stock_name)
    return msg
