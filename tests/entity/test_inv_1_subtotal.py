"""INV-1: subtotal(items) == Σ(price × qty)"""

import pytest

from src.cart import subtotal

pytestmark = pytest.mark.entity


def test_inv_1_01_single_item_subtotal_equals_price_times_qty():
    """INV-1: 단일 품목 소계는 price × qty와 같다."""
    items = [{"price": 10000, "qty": 2}]

    assert subtotal(items) == 20000


def test_inv_1_02_discovery_scenario_subtotal_equals_66000():
    """INV-1: Discovery 시나리오(A×3 + B×1) 소계는 66,000원이다."""
    item_a = {"sku": "A", "price": 12000, "qty": 3}
    item_b = {"sku": "B", "price": 30000, "qty": 1}

    assert subtotal([item_a, item_b]) == 66000


def test_inv_1_03_multiple_items_subtotal_equals_sum_of_price_times_qty():
    """INV-1: 복수 품목 소계는 각 price × qty의 합과 같다."""
    items = [{"price": 5000, "qty": 1}, {"price": 3000, "qty": 4}]

    assert subtotal(items) == 17000
