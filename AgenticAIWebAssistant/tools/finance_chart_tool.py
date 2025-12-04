import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64
import os
from io import BytesIO
from tools.finance_core import get_chart_df

def _fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    b = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    return b

def get_stock_chart_markdown(stock_name: str) -> str:
    symbol, df = get_chart_df(stock_name, period="30d")
    if df is None or df.empty:
        return f"No valid data available for '{symbol}'"
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df.index, df['Close'], marker='o', linestyle='-')
    ax.set_title(f"30-Day Closing Price for {symbol}")
    ax.set_xlabel("Date"); ax.set_ylabel("Price (INR)")
    ax.grid(True)
    fig.tight_layout()
    #b64 = _fig_to_base64(fig)
    #plt.close(fig)
    #return f"Here is the chart for {stock_name} (last 30 days):\n\n![](data:image/png;base64,{b64})"
    chart_path = f"charts/{symbol}_chart.png"
    os.makedirs("charts", exist_ok=True)
    plt.savefig(chart_path)
    plt.close()
    return f"🖼 Chart for '{stock_name}' ({symbol}) saved at: {chart_path}"
