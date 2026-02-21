import pandas as pd

from trading_indicators.base import Indicator
from trading_indicators.registry import register


@register
class BollingerBands(Indicator):
    name = "bollinger"
    params = {"period": 20, "std_dev": 2}

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        p = self._get_params(**kwargs)
        period = p["period"]
        num_std = p["std_dev"]
        result = df.copy()

        sma = df["close"].rolling(window=period).mean()
        std = df["close"].rolling(window=period).std()

        result["bb_middle"] = sma
        result["bb_upper"] = sma + num_std * std
        result["bb_lower"] = sma - num_std * std
        return result
