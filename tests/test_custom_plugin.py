import tempfile
import textwrap
from pathlib import Path

import numpy as np
import pandas as pd

from trading_indicators import discover_plugins, get, list_indicators


def test_discover_plugins_from_directory():
    plugin_code = textwrap.dedent("""\
        import pandas as pd
        from trading_indicators.base import Indicator
        from trading_indicators.registry import register

        @register
        class VWAP(Indicator):
            name = "vwap"
            params = {}

            def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
                result = df.copy()
                cumvol = df["volume"].cumsum()
                result["vwap"] = (df["close"] * df["volume"]).cumsum() / cumvol
                return result
    """)

    with tempfile.TemporaryDirectory() as tmpdir:
        plugin_file = Path(tmpdir) / "vwap_indicator.py"
        plugin_file.write_text(plugin_code)

        discover_plugins(tmpdir)

        assert "vwap" in list_indicators()
        ind = get("vwap")

        df = pd.DataFrame({
            "open": [10, 11, 12],
            "high": [11, 12, 13],
            "low": [9, 10, 11],
            "close": [10.5, 11.5, 12.5],
            "volume": [100, 200, 300],
        })
        result = ind.compute(df)
        assert "vwap" in result.columns
        assert len(result) == 3


def test_discover_plugins_skips_dunder_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        init_file = Path(tmpdir) / "__init__.py"
        init_file.write_text("# should be skipped")

        before = set(list_indicators())
        discover_plugins(tmpdir)
        after = set(list_indicators())
        assert before == after
