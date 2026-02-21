import pandas as pd
import pytest

from trading_indicators import Backtest, BacktestResult, Strategy, generate_ohlcv


@pytest.fixture
def ohlcv_df():
    return generate_ohlcv(days=252, seed=42)


class TestGenerateOHLCV:
    def test_shape_and_columns(self):
        df = generate_ohlcv(days=100, seed=0)
        assert len(df) == 100
        assert list(df.columns) == ["open", "high", "low", "close", "volume"]

    def test_deterministic(self):
        df1 = generate_ohlcv(seed=7)
        df2 = generate_ohlcv(seed=7)
        pd.testing.assert_frame_equal(df1, df2)


class TestBacktestRSI:
    def test_rsi_strategy_runs(self, ohlcv_df):
        strategy = Strategy(
            name="RSI Mean Reversion",
            indicator="rsi",
            indicator_params={"period": 14},
            entry_signal=lambda df: df["rsi"] < 30,
            exit_signal=lambda df: df["rsi"] > 70,
        )
        result = Backtest(ohlcv_df, strategy).run()
        assert isinstance(result, BacktestResult)
        assert result.num_trades >= 0
        assert 0.0 <= result.win_rate <= 1.0

    def test_rsi_trades_have_required_keys(self, ohlcv_df):
        strategy = Strategy(
            name="RSI",
            indicator="rsi",
            indicator_params={},
            entry_signal=lambda df: df["rsi"] < 30,
            exit_signal=lambda df: df["rsi"] > 70,
        )
        result = Backtest(ohlcv_df, strategy).run()
        for trade in result.trades:
            assert "entry_date" in trade
            assert "exit_date" in trade
            assert "entry_price" in trade
            assert "exit_price" in trade
            assert "return" in trade


class TestBacktestSMA:
    def test_sma_crossover(self, ohlcv_df):
        strategy = Strategy(
            name="SMA Crossover",
            indicator="sma",
            indicator_params={"period": 20},
            entry_signal=lambda df: df["close"] > df["sma_20"],
            exit_signal=lambda df: df["close"] < df["sma_20"],
        )
        result = Backtest(ohlcv_df, strategy).run()
        assert isinstance(result, BacktestResult)
        assert result.num_trades > 0


class TestNoTrades:
    def test_no_entry_signals(self, ohlcv_df):
        strategy = Strategy(
            name="Never Enter",
            indicator="sma",
            indicator_params={"period": 20},
            entry_signal=lambda df: pd.Series(False, index=df.index),
            exit_signal=lambda df: pd.Series(True, index=df.index),
        )
        result = Backtest(ohlcv_df, strategy).run()
        assert result.num_trades == 0
        assert result.total_return == 0.0
        assert result.win_rate == 0.0
        assert result.trades == []


class TestBacktestResult:
    def test_summary_format(self):
        result = BacktestResult(
            trades=[{"return": 0.05}, {"return": -0.02}],
            total_return=0.029,
            win_rate=0.5,
            num_trades=2,
        )
        summary = result.summary()
        assert "Total trades:  2" in summary
        assert "50.00%" in summary
        assert "2.90%" in summary

    def test_defaults(self):
        result = BacktestResult()
        assert result.trades == []
        assert result.num_trades == 0
        assert result.total_return == 0.0
        assert result.win_rate == 0.0
