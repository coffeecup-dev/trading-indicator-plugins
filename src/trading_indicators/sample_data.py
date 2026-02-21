import numpy as np
import pandas as pd


def generate_ohlcv(days: int = 252, seed: int = 42) -> pd.DataFrame:
    """Generate realistic synthetic OHLCV data using a random walk.

    Parameters
    ----------
    days : int
        Number of trading days to generate (default 252, ~1 year).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame with datetime index and columns:
        open, high, low, close, volume.
    """
    rng = np.random.default_rng(seed)

    # Start price around 100
    price = 100.0
    opens, highs, lows, closes, volumes = [], [], [], [], []

    for _ in range(days):
        open_price = price
        # Daily return: slight upward drift + noise
        daily_return = rng.normal(0.0005, 0.02)
        close_price = open_price * (1 + daily_return)

        # Intraday high/low
        intraday_range = abs(close_price - open_price) + open_price * rng.uniform(0.002, 0.015)
        high_price = max(open_price, close_price) + intraday_range * rng.uniform(0.1, 0.6)
        low_price = min(open_price, close_price) - intraday_range * rng.uniform(0.1, 0.6)

        opens.append(round(open_price, 2))
        highs.append(round(high_price, 2))
        lows.append(round(low_price, 2))
        closes.append(round(close_price, 2))
        volumes.append(int(rng.integers(500_000, 5_000_000)))

        # Next day opens near previous close
        price = close_price

    dates = pd.bdate_range(start="2020-01-02", periods=days)
    return pd.DataFrame(
        {"open": opens, "high": highs, "low": lows, "close": closes, "volume": volumes},
        index=dates,
    )
