import yfinance as yf
import pandas as pd
from utils.symbols import get_stock_symbol

def safe_download(symbol: str, period: str = "30d", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=True, progress=False)
    if isinstance(df, pd.DataFrame):
        return df
    return pd.DataFrame()

def fetch_quote(symbol: str) -> dict:
    t = yf.Ticker(symbol)
    info = {}
    try:
        info = t.fast_info if hasattr(t, "fast_info") else {}
    except Exception:
        info = {}
    price = None
    try:
        if isinstance(info, dict):
            price = info.get("last_price") or info.get("lastPrice") or info.get("last_price")
        else:
            price = getattr(info, "last_price", None)
    except Exception:
        price = None
    if price is None:
        hist = t.history(period="1d")
        if not hist.empty and "Close" in hist:
            price = float(hist["Close"].iloc[-1])
    market_cap = None
    pe = None
    vol = None
    try:
        if isinstance(info, dict):
            market_cap = info.get("market_cap") or info.get("marketCap") or info.get("market_cap")
            pe = info.get("trailing_pe") or info.get("trailingPE") or info.get("pe_ratio")
            vol = info.get("last_volume") or info.get("lastVolume") or info.get("volume")
        else:
            market_cap = getattr(info, "market_cap", None)
            pe = getattr(info, "pe_ratio", None)
            vol = getattr(info, "last_volume", None)
    except Exception:
        pass
    return {"price": price, "market_cap": market_cap, "pe_ratio": pe, "volume": vol}

def format_money(val) -> str:
    if val is None:
        return "N/A"
    try:
        v = float(val)
    except Exception:
        return "N/A"
    for unit in ["", "K", "M", "B", "T"]:
        if abs(v) < 1000.0:
            return f"{v:,.0f}{unit}"
        v /= 1000.0
    return f"{v:.1f}P"

def get_financials(stock_name: str) -> tuple:
    symbol = get_stock_symbol(stock_name)
    print(f"[INFO] Looking up: {symbol}")
    quote = fetch_quote(symbol)
    msg = (
        f"📊 Financial data for '{stock_name}' ({symbol}):\n"
        f"- Price: ₹{quote['price'] if quote['price'] is not None else 'N/A'}\n"
        f"- Market Cap: {format_money(quote['market_cap'])}\n"
        f"- P/E Ratio: {quote['pe_ratio'] if quote['pe_ratio'] is not None else 'N/A'}\n"
        f"- Volume: {quote['volume'] if quote['volume'] is not None else 'N/A'}"
    )
    return msg, {"symbol": symbol, **quote}

def get_chart_df(stock_name: str, period: str = "30d"):
    symbol = get_stock_symbol(stock_name)
    print(f"[INFO] Fetching chart for: {symbol}")
    df = safe_download(symbol, period=period, interval="1d")
    return symbol, df
