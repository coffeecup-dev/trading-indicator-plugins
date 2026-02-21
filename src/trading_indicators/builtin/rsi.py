import pandas as pd

from trading_indicators.base import Indicator
from trading_indicators.registry import register


@register
class RSI(Indicator):
    name = "rsi"
    params = {"period": 14}

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        p = self._get_params(**kwargs)
        period = p["period"]
        result = df.copy()

        delta = df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        # Wilder's smoothing (equivalent to EWM with alpha=1/period)
        avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

        rs = avg_gain / avg_loss
        result["rsi"] = 100 - (100 / (1 + rs))
        return result
