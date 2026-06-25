"""INV-4: 모든 입력에서 0 ≤ final_total ≤ subtotal. 할인은 금액을 늘리지 않는다."""

import pytest

from src.cart import subtotal

pytestmark = pytest.mark.entity

ITEM_A = {"sku": "A", "price": 12000, "qty": 3}
ITEM_B = {"sku": "B", "price": 30000, "qty": 1}
DISCOVERY_ITEMS = [ITEM_A, ITEM_B]

BELOW_THRESHOLD_ITEMS = [{"price": 12000, "qty": 4}]  # 48,000


@pytest.mark.parametrize(
    "items,is_vip",
    [
        (DISCOVERY_ITEMS, False),
        (DISCOVERY_ITEMS, True),
        (BELOW_THRESHOLD_ITEMS, False),
        (BELOW_THRESHOLD_ITEMS, True),
    ],
)
def test_inv_4_01_final_total_is_non_negative(items, is_vip):
    """INV-4: 유효한 입력에서 final_total >= 0 이다."""
    from src.cart import calculate_total

    assert calculate_total(items, is_vip=is_vip) >= 0


@pytest.mark.parametrize(
    "items,is_vip",
    [
        (DISCOVERY_ITEMS, False),
        (DISCOVERY_ITEMS, True),
        (BELOW_THRESHOLD_ITEMS, False),
        (BELOW_THRESHOLD_ITEMS, True),
    ],
)
def test_inv_4_02_final_total_does_not_exceed_subtotal(items, is_vip):
    """INV-4: 유효한 입력에서 final_total <= subtotal 이다."""
    from src.cart import calculate_total

    base = subtotal(items)
    final = calculate_total(items, is_vip=is_vip)

    assert final <= base
