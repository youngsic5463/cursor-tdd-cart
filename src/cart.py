def _validate_line_items(items):
    for index, item in enumerate(items):
        price = item["price"]
        qty = item["qty"]
        if price < 0 or qty < 0:  # E-2
            raise ValueError(f"negative price or qty at index {index}")


def subtotal(items):
    if items is None:  # E-1
        raise TypeError("items must not be None")

    _validate_line_items(items)

    total = 0
    for item in items:
        price = item["price"]
        qty = item["qty"]
        total += price * qty  # INV-1

    return total


THRESHOLD = 50000
THRESHOLD_RATE = 0.9
VIP_RATE = 0.95


def apply_threshold_discount(amount):
    if amount >= THRESHOLD:  # INV-2
        return round(amount * THRESHOLD_RATE)  # INV-2

    return amount  # INV-2


def final_total(items, is_vip=False):
    base = subtotal(items)  # INV-4
    amount = apply_threshold_discount(base)  # INV-3
    if is_vip:
        return round(amount * VIP_RATE)  # INV-3

    return amount  # INV-4


apply_threshold = apply_threshold_discount
calculate_total = final_total
