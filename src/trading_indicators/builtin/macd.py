import pandas as pd

from trading_indicators.base import Indicator
from trading_indicators.registry import register


@register
class MACD(Indicator):
    name = "macd"
    params = {"fast": 12, "slow": 26, "signal": 9}

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        p = self._get_params(**kwargs)
        fast, slow, signal_period = p["fast"], p["slow"], p["signal"]
        result = df.copy()

        ema_fast = df["close"].ewm(span=fast, adjust=False).mean()
        ema_slow = df["close"].ewm(span=slow, adjust=False).mean()

        result["macd_line"] = ema_fast - ema_slow
        result["macd_signal"] = result["macd_line"].ewm(span=signal_period, adjust=False).mean()
        result["macd_histogram"] = result["macd_line"] - result["macd_signal"]
        return result
