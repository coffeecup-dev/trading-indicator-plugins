from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import pandas as pd

from trading_indicators.registry import get


@dataclass
class Strategy:
    """Defines an indicator-based trading strategy."""

    name: str
    indicator: str
    indicator_params: dict
    entry_signal: Callable[[pd.DataFrame], pd.Series]
    exit_signal: Callable[[pd.DataFrame], pd.Series]


@dataclass
class BacktestResult:
    """Holds the results of a backtest run."""

    trades: list[dict] = field(default_factory=list)
    total_return: float = 0.0
    win_rate: float = 0.0
    num_trades: int = 0

    def summary(self) -> str:
        """Return a formatted text summary of the backtest results."""
        lines = [
            "Backtest Summary",
            "=" * 40,
            f"Total trades:  {self.num_trades}",
            f"Win rate:      {self.win_rate:.2%}",
            f"Total return:  {self.total_return:.2%}",
            "=" * 40,
        ]
        return "\n".join(lines)


class Backtest:
    """Simple long-only backtest engine.

    Computes an indicator on the OHLCV data, then walks through the
    entry/exit signals to simulate trades (buy/sell at close, one
    position at a time).
    """

    def __init__(self, df: pd.DataFrame, strategy: Strategy) -> None:
        self.df = df.copy()
        self.strategy = strategy

    def run(self) -> BacktestResult:
        """Execute the backtest and return results."""
        indicator = get(self.strategy.indicator)
        df = indicator.compute(self.df, **self.strategy.indicator_params)

        entries = self.strategy.entry_signal(df)
        exits = self.strategy.exit_signal(df)

        trades: list[dict] = []
        in_position = False
        entry_date = None
        entry_price = 0.0

        for i in range(len(df)):
            if not in_position and entries.iloc[i]:
                in_position = True
                entry_date = df.index[i]
                entry_price = df["close"].iloc[i]
            elif in_position and exits.iloc[i]:
                exit_date = df.index[i]
                exit_price = df["close"].iloc[i]
                trade_return = (exit_price - entry_price) / entry_price
                trades.append(
                    {
                        "entry_date": entry_date,
                        "exit_date": exit_date,
                        "entry_price": entry_price,
                        "exit_price": exit_price,
                        "return": trade_return,
                    }
                )
                in_position = False

        num_trades = len(trades)
        if num_trades > 0:
            wins = sum(1 for t in trades if t["return"] > 0)
            win_rate = wins / num_trades
            # Compound returns
            total_return = 1.0
            for t in trades:
                total_return *= 1 + t["return"]
            total_return -= 1.0
        else:
            win_rate = 0.0
            total_return = 0.0

        return BacktestResult(
            trades=trades,
            total_return=total_return,
            win_rate=win_rate,
            num_trades=num_trades,
        )
