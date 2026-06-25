"""E-1, E-2: subtotal() 입력 검증 계약"""

import pytest

from src.cart import subtotal

pytestmark = pytest.mark.boundary


def test_e_1_none_items_raises_type_error():
    """E-1: subtotal(None)은 TypeError를 던진다."""
    with pytest.raises(TypeError):
        subtotal(None)


def test_e_2_negative_qty_raises_value_error_with_index():
    """E-2: 음수 qty는 ValueError를 던지고 메시지에 인덱스가 포함된다."""
    with pytest.raises(ValueError, match=r"index\s+0"):
        subtotal([{"price": 1000, "qty": -1}])


def test_e_2_negative_price_raises_value_error_with_index():
    """E-2: 음수 price는 ValueError를 던지고 메시지에 인덱스가 포함된다."""
    with pytest.raises(ValueError, match=r"index\s+0"):
        subtotal([{"price": -500, "qty": 1}])
