import pytest

from trading_indicators import Indicator, get, list_indicators, register


def test_list_indicators_contains_builtins():
    names = list_indicators()
    assert "sma" in names
    assert "ema" in names
    assert "rsi" in names
    assert "macd" in names
    assert "bollinger" in names


def test_get_returns_indicator_instance():
    ind = get("sma")
    assert isinstance(ind, Indicator)


def test_get_unknown_raises():
    with pytest.raises(KeyError, match="not found"):
        get("nonexistent_indicator")


def test_register_custom_indicator():
    @register
    class MyCustom(Indicator):
        name = "test_custom"
        params = {"x": 1}

        def compute(self, df, **kwargs):
            return df

    assert "test_custom" in list_indicators()
    inst = get("test_custom")
    assert inst.name == "test_custom"
