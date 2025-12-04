import re

SYMBOL_MAP = {
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
    "infy": "INFY.NS",
    "wipro": "WIPRO.NS",
    "hdfcbank": "HDFCBANK.NS",
    "hdfc bank": "HDFCBANK.NS",
    "bel": "BEL.NS",
    "bse": "BSE.NS",
    "rvnl": "RVNL.NS",
    "itc": "ITC.NS",
}

def normalize_company_name(text: str) -> str:
    parts = re.findall(r"[A-Za-z]+", text or "")
    name = "".join(parts[:3]).lower()
    for suf in ("limited","ltd","corporation","corp","company","co","plc"):
        name = name.replace(suf, "")
    return name.strip()

def get_stock_symbol(stock_name: str) -> str:
    if not stock_name:
        return "UNKNOWN.NS"
    key = normalize_company_name(stock_name)
    if key in SYMBOL_MAP:
        return SYMBOL_MAP[key]
    # fallback: take first token and append .NS
    raw = re.findall(r"[A-Za-z]+", stock_name)
    if raw:
        return raw[0].upper() + ".NS"
    return "UNKNOWN.NS"
