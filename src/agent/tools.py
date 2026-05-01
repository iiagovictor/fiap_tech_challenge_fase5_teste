"""
Financial analysis tools for the LLM agent.

Provides tools for:
- Technical analysis calculation
- Price trend analysis
- Market sentiment indicators
"""

import logging
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


def get_stock_price_history(ticker: str, period: str = "1mo") -> dict:
    """
    Get historical stock price data.
    
    Args:
        ticker: Stock ticker symbol (e.g., ITUB4.SA)
        period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    
    Returns:
        Dictionary with price history and summary statistics
    """
    logger.info(f"Fetching price history for {ticker} (period: {period})")

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return {"error": f"No data found for ticker {ticker}"}

        # Calculate summary statistics
        current_price = float(hist["Close"].iloc[-1])
        start_price = float(hist["Close"].iloc[0])
        high_price = float(hist["High"].max())
        low_price = float(hist["Low"].min())
        avg_volume = float(hist["Volume"].mean())

        price_change = current_price - start_price
        price_change_pct = (price_change / start_price) * 100

        return {
            "ticker": ticker,
            "period": period,
            "current_price": round(current_price, 2),
            "start_price": round(start_price, 2),
            "high_price": round(high_price, 2),
            "low_price": round(low_price, 2),
            "price_change": round(price_change, 2),
            "price_change_pct": round(price_change_pct, 2),
            "avg_volume": int(avg_volume),
            "data_points": len(hist),
        }

    except Exception as e:
        logger.error(f"Error fetching price history: {e}")
        return {"error": str(e)}


def calculate_technical_indicators(ticker: str, period: str = "3mo") -> dict:
    """
    Calculate technical indicators for a stock.
    
    Returns RSI, MACD, Moving Averages, and Bollinger Bands.
    
    Args:
        ticker: Stock ticker symbol
        period: Time period for calculation
    
    Returns:
        Dictionary with technical indicators
    """
    logger.info(f"Calculating technical indicators for {ticker}")

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty or len(hist) < 50:
            return {"error": f"Insufficient data for {ticker}"}

        close = hist["Close"]

        # RSI (14-day)
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = float(rsi.iloc[-1])

        # Moving Averages
        sma_20 = float(close.rolling(window=20).mean().iloc[-1])
        sma_50 = float(close.rolling(window=50).mean().iloc[-1])
        ema_12 = float(close.ewm(span=12, adjust=False).mean().iloc[-1])
        ema_26 = float(close.ewm(span=26, adjust=False).mean().iloc[-1])

        # MACD
        macd_line = ema_12 - ema_26
        signal_line = float(close.ewm(span=12).mean().ewm(span=26).mean().iloc[-1])
        macd = macd_line

        # Bollinger Bands
        bb_middle = close.rolling(window=20).mean()
        bb_std = close.rolling(window=20).std()
        bb_upper = bb_middle + (2 * bb_std)
        bb_lower = bb_middle - (2 * bb_std)

        current_price = float(close.iloc[-1])

        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "rsi_14": round(current_rsi, 2),
            "sma_20": round(sma_20, 2),
            "sma_50": round(sma_50, 2),
            "ema_12": round(ema_12, 2),
            "ema_26": round(ema_26, 2),
            "macd": round(macd, 2),
            "bb_upper": round(float(bb_upper.iloc[-1]), 2),
            "bb_middle": round(float(bb_middle.iloc[-1]), 2),
            "bb_lower": round(float(bb_lower.iloc[-1]), 2),
            "signal": _interpret_indicators(current_rsi, current_price, sma_20, sma_50),
        }

    except Exception as e:
        logger.error(f"Error calculating indicators: {e}")
        return {"error": str(e)}


def _interpret_indicators(rsi: float, price: float, sma_20: float, sma_50: float) -> str:
    """Interpret technical indicators to generate a signal."""
    signals = []

    # RSI interpretation
    if rsi > 70:
        signals.append("overbought")
    elif rsi < 30:
        signals.append("oversold")
    else:
        signals.append("neutral RSI")

    # Price vs Moving Averages
    if price > sma_20 > sma_50:
        signals.append("bullish trend")
    elif price < sma_20 < sma_50:
        signals.append("bearish trend")
    else:
        signals.append("mixed trend")

    return ", ".join(signals)


def compare_stocks(tickers: list[str], period: str = "1mo") -> dict:
    """
    Compare performance of multiple stocks.
    
    Args:
        tickers: List of ticker symbols
        period: Time period for comparison
    
    Returns:
        Dictionary with comparative analysis
    """
    logger.info(f"Comparing stocks: {tickers}")

    results = []
    for ticker in tickers:
        price_data = get_stock_price_history(ticker, period)
        if "error" not in price_data:
            results.append(price_data)

    if not results:
        return {"error": "No valid data for comparison"}

    # Sort by performance
    results_sorted = sorted(results, key=lambda x: x["price_change_pct"], reverse=True)

    return {
        "period": period,
        "stocks_compared": len(results_sorted),
        "best_performer": results_sorted[0]["ticker"],
        "worst_performer": results_sorted[-1]["ticker"],
        "results": results_sorted,
    }


# Tool metadata for LLM agent
TOOLS = [
    {
        "name": "get_stock_price_history",
        "description": "Get historical price data and statistics for a stock",
        "parameters": {
            "ticker": {"type": "string", "description": "Stock ticker symbol"},
            "period": {"type": "string", "description": "Time period (1mo, 3mo, 1y, etc.)"},
        },
        "function": get_stock_price_history,
    },
    {
        "name": "calculate_technical_indicators",
        "description": "Calculate technical analysis indicators (RSI, MACD, Moving Averages)",
        "parameters": {
            "ticker": {"type": "string", "description": "Stock ticker symbol"},
            "period": {"type": "string", "description": "Time period for calculation"},
        },
        "function": calculate_technical_indicators,
    },
    {
        "name": "compare_stocks",
        "description": "Compare performance of multiple stocks",
        "parameters": {
            "tickers": {"type": "array", "description": "List of ticker symbols"},
            "period": {"type": "string", "description": "Time period for comparison"},
        },
        "function": compare_stocks,
    },
]


if __name__ == "__main__":
    # Test tools
    logging.basicConfig(level=logging.INFO)

    print("\n📊 Testing Financial Tools\n")

    # Test 1: Price history
    print("1. Price History:")
    result = get_stock_price_history("ITUB4.SA", period="1mo")
    print(f"   {result}\n")

    # Test 2: Technical indicators
    print("2. Technical Indicators:")
    result = calculate_technical_indicators("ITUB4.SA", period="3mo")
    print(f"   {result}\n")

    # Test 3: Compare stocks
    print("3. Stock Comparison:")
    result = compare_stocks(["ITUB4.SA", "PETR4.SA"], period="1mo")
    print(f"   {result}\n")
