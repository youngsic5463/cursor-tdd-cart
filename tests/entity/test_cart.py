"""INV-1: subtotal(items) == Σ(price × qty)
INV-2: amount ≥ 50000 → round(amount×0.9) / < 50000 → 그대로 (경계 포함)
"""

import pytest

from src.cart import subtotal

pytestmark = pytest.mark.entity


def test_inv_1_subtotal_equals_sum_of_price_times_qty():
    """INV-1: subtotal([{price:1000,qty:3},{price:2000,qty:2}]) == 7000"""
    items = [{"price": 1000, "qty": 3}, {"price": 2000, "qty": 2}]

    assert subtotal(items) == 7000


def test_inv_2_apply_threshold_discount_at_boundary_includes_discount():
    """INV-2: apply_threshold_discount(50000) == 45000 (경계 포함)"""
    from src.cart import apply_threshold_discount

    assert apply_threshold_discount(50000) == 45000


def test_inv_2_apply_threshold_discount_below_threshold_unchanged():
    """INV-2: apply_threshold_discount(49999) == 49999 (할인 없음)"""
    from src.cart import apply_threshold_discount

    assert apply_threshold_discount(49999) == 49999
