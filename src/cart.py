def subtotal(items):
    if items is None:  # E-1
        raise TypeError("items must not be None")

    total = 0
    for index, item in enumerate(items):
        price = item["price"]
        qty = item["qty"]
        if price < 0 or qty < 0:  # E-2
            raise ValueError(f"negative price or qty at index {index}")
        total += price * qty  # INV-1

    return total
