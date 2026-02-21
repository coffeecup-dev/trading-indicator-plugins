import pandas as pd

from trading_indicators.base import Indicator
from trading_indicators.registry import register


@register
class SMA(Indicator):
    name = "sma"
    params = {"period": 20}

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        p = self._get_params(**kwargs)
        period = p["period"]
        result = df.copy()
        result[f"sma_{period}"] = df["close"].rolling(window=period).mean()
        return result
