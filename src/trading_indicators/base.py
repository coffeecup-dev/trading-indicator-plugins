from abc import ABC, abstractmethod

import pandas as pd


class Indicator(ABC):
    """Abstract base class for all trading indicators."""

    name: str = ""
    params: dict = {}

    @abstractmethod
    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Compute the indicator on an OHLCV DataFrame.

        Args:
            df: DataFrame with columns: open, high, low, close, volume
            **kwargs: Override default params for this computation.

        Returns:
            DataFrame with original columns plus new indicator column(s).
        """

    def _get_params(self, **kwargs):
        """Merge default params with runtime overrides."""
        merged = {**self.params, **kwargs}
        return merged
