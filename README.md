# trading-indicator-plugins

A plugin-based Python library for computing trading indicators on OHLCV DataFrames.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
import pandas as pd
from trading_indicators import get, list_indicators

# See available indicators
print(list_indicators())
# ['bollinger', 'ema', 'macd', 'rsi', 'sma']

# Compute RSI on an OHLCV DataFrame
rsi = get("rsi")
result = rsi.compute(df, period=21)
```

## Built-in Indicators

| Indicator | Name | Default Parameters | Output Columns |
|-----------|------|--------------------|----------------|
| Simple Moving Average | `sma` | `period=20` | `sma_{period}` |
| Exponential Moving Average | `ema` | `period=20` | `ema_{period}` |
| Relative Strength Index | `rsi` | `period=14` | `rsi` |
| MACD | `macd` | `fast=12, slow=26, signal=9` | `macd_line`, `macd_signal`, `macd_histogram` |
| Bollinger Bands | `bollinger` | `period=20, std_dev=2` | `bb_upper`, `bb_middle`, `bb_lower` |

## Custom Plugins

Create a `.py` file with an `Indicator` subclass decorated with `@register`:

```python
import pandas as pd
from trading_indicators import Indicator, register

@register
class VWAP(Indicator):
    name = "vwap"
    params = {}

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        result = df.copy()
        cumvol = df["volume"].cumsum()
        result["vwap"] = (df["close"] * df["volume"]).cumsum() / cumvol
        return result
```

Then load plugins from a directory at runtime:

```python
from trading_indicators import discover_plugins

discover_plugins("/path/to/my/plugins")
```

## Input Format

All indicators expect a pandas DataFrame with these columns: `open`, `high`, `low`, `close`, `volume`.

## Development

```bash
pip install -e ".[dev]"
pytest tests/
```
