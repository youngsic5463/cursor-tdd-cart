"""INV-2: amount ≥ 50000 → round(amount×0.9) / < 50000 → 그대로 (경계 포함)"""

import pytest

pytestmark = pytest.mark.entity


def test_inv_2_01_amount_below_threshold_unchanged():
    """INV-2: amount < 50000이면 원래 금액을 그대로 반환한다."""
    from src.cart import apply_threshold

    assert apply_threshold(48000) == 48000


def test_inv_2_02_amount_at_threshold_applies_ten_percent_discount():
    """INV-2: amount == 50000이면 round(amount × 0.9)를 반환한다 (경계 포함)."""
    from src.cart import apply_threshold

    assert apply_threshold(50000) == 45000


def test_inv_2_03_amount_above_threshold_applies_ten_percent_discount():
    """INV-2: amount >= 50000이면 round(amount × 0.9)를 반환한다."""
    from src.cart import apply_threshold

    assert apply_threshold(60000) == 54000
