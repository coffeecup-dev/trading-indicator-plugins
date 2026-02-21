import numpy as np
import pandas as pd
import pytest

from trading_indicators import get


@pytest.fixture
def ohlcv_df():
    np.random.seed(42)
    n = 100
    close = 100 + np.cumsum(np.random.randn(n) * 0.5)
    return pd.DataFrame({
        "open": close + np.random.randn(n) * 0.1,
        "high": close + abs(np.random.randn(n) * 0.3),
        "low": close - abs(np.random.randn(n) * 0.3),
        "close": close,
        "volume": np.random.randint(1000, 10000, n),
    })


class TestSMA:
    def test_default_period(self, ohlcv_df):
        result = get("sma").compute(ohlcv_df)
        assert "sma_20" in result.columns
        assert result["sma_20"].isna().sum() == 19  # first 19 are NaN

    def test_custom_period(self, ohlcv_df):
        result = get("sma").compute(ohlcv_df, period=5)
        assert "sma_5" in result.columns
        # Verify calculation: last value should be mean of last 5 closes
        expected = ohlcv_df["close"].iloc[-5:].mean()
        assert abs(result["sma_5"].iloc[-1] - expected) < 1e-10


class TestEMA:
    def test_default_period(self, ohlcv_df):
        result = get("ema").compute(ohlcv_df)
        assert "ema_20" in result.columns
        assert not result["ema_20"].isna().any()

    def test_custom_period(self, ohlcv_df):
        result = get("ema").compute(ohlcv_df, period=10)
        assert "ema_10" in result.columns


class TestRSI:
    def test_default(self, ohlcv_df):
        result = get("rsi").compute(ohlcv_df)
        assert "rsi" in result.columns
        # RSI should be between 0 and 100 (excluding NaN rows)
        valid = result["rsi"].dropna()
        assert (valid >= 0).all() and (valid <= 100).all()

    def test_custom_period(self, ohlcv_df):
        result = get("rsi").compute(ohlcv_df, period=21)
        assert "rsi" in result.columns


class TestMACD:
    def test_default(self, ohlcv_df):
        result = get("macd").compute(ohlcv_df)
        assert "macd_line" in result.columns
        assert "macd_signal" in result.columns
        assert "macd_histogram" in result.columns

    def test_histogram_is_diff(self, ohlcv_df):
        result = get("macd").compute(ohlcv_df)
        diff = result["macd_line"] - result["macd_signal"]
        pd.testing.assert_series_equal(result["macd_histogram"], diff, check_names=False)


class TestBollinger:
    def test_default(self, ohlcv_df):
        result = get("bollinger").compute(ohlcv_df)
        assert "bb_middle" in result.columns
        assert "bb_upper" in result.columns
        assert "bb_lower" in result.columns

    def test_upper_above_lower(self, ohlcv_df):
        result = get("bollinger").compute(ohlcv_df)
        valid = result.dropna()
        assert (valid["bb_upper"] >= valid["bb_lower"]).all()

    def test_middle_is_sma(self, ohlcv_df):
        result = get("bollinger").compute(ohlcv_df, period=20)
        expected_sma = ohlcv_df["close"].rolling(20).mean()
        pd.testing.assert_series_equal(result["bb_middle"], expected_sma, check_names=False)
