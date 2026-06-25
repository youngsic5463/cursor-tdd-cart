"""INV-1: subtotal(items) == Σ(price × qty)
INV-2: amount ≥ 50000 → round(amount×0.9) / < 50000 → 그대로 (경계 포함)
INV-3: final = 문턱할인 적용 후, VIP면 round(×0.95). 순서 문턱→VIP 고정
INV-4: 모든 입력에서 0 ≤ final_total ≤ subtotal. 할인은 금액을 늘리지 않는다
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


def test_inv_3_final_total_vip_applies_threshold_then_vip_discount():
    """INV-3: final_total([{price:60000,qty:1}], is_vip=True) == 51300 (60000→54000→51300)"""
    from src.cart import final_total

    assert final_total([{"price": 60000, "qty": 1}], is_vip=True) == 51300


@pytest.mark.parametrize(
    "items,is_vip",
    [
        ([], False),
        ([], True),
        ([{"price": 49999, "qty": 1}], False),
        ([{"price": 49999, "qty": 1}], True),
        ([{"price": 50000, "qty": 1}], False),
        ([{"price": 50000, "qty": 1}], True),
    ],
)
def test_inv_4_final_total_within_bounds(items, is_vip):
    """INV-4: 0 <= final_total <= subtotal (빈 장바구니, 49999, 50000, VIP/비VIP)"""
    from src.cart import final_total

    base = subtotal(items)
    final = final_total(items, is_vip=is_vip)

    assert 0 <= final <= base
