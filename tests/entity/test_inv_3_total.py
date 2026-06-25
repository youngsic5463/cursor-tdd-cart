"""INV-3: final = 문턱할인 적용 후, VIP면 round(×0.95). 순서 문턱→VIP 고정"""

import pytest

pytestmark = pytest.mark.entity

ITEM_A = {"sku": "A", "price": 12000, "qty": 3}
ITEM_B = {"sku": "B", "price": 30000, "qty": 1}
DISCOVERY_ITEMS = [ITEM_A, ITEM_B]


def test_inv_3_01_non_vip_applies_threshold_only():
    """INV-3: non-VIP는 문턱 할인만 적용한다 (순서: 문턱→VIP)."""
    from src.cart import calculate_total

    assert calculate_total(DISCOVERY_ITEMS, is_vip=False) == 59400


def test_inv_3_02_vip_applies_threshold_then_vip_discount():
    """INV-3: VIP는 문턱 할인 후 round(×0.95)를 적용한다."""
    from src.cart import calculate_total

    assert calculate_total(DISCOVERY_ITEMS, is_vip=True) == 56430
