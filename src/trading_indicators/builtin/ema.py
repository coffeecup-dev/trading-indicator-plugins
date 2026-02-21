import pandas as pd

from trading_indicators.base import Indicator
from trading_indicators.registry import register


@register
class EMA(Indicator):
    name = "ema"
    params = {"period": 20}

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        p = self._get_params(**kwargs)
        period = p["period"]
        result = df.copy()
        result[f"ema_{period}"] = df["close"].ewm(span=period, adjust=False).mean()
        return result
