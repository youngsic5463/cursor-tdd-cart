# Test Plan — INV-1, E-1, E-2

| 항목 | 내용 |
|------|------|
| 대상 계약 | INV-1, E-1, E-2 |
| 근거 | [README.md](../README.md) |
| 구현 대상 | `src/cart.py` — `subtotal()` |
| TDD 순서 | **INV-1 → E-1 → E-2** (README 권장 RED 순서 중 해당 구간) |

---

## 계약 요약

| ID | 계약 | 계층 | 테스트 파일 |
|----|------|------|-------------|
| INV-1 | `subtotal(items) == Σ(price × qty)` | Entity | `tests/entity/test_inv_1_subtotal.py` |
| E-1 | `items is None → TypeError` | Boundary* | `tests/boundary/test_e_1_items_none.py` |
| E-2 | `price` 또는 `qty`가 음수 → `ValueError`, 인덱스 포함 | Boundary* | `tests/boundary/test_e_2_negative_price_or_qty.py` |

> **Boundary*** — 본 실습에서는 Flask 폼 없이 `cart.py` 도메인 진입점에서 검증한다.

---

## 1. INV-1 — 소계 계산

### 1.1 목적

품목 목록 `items`에 대해 소계가 각 품목의 `price × qty` 합과 **항상** 같음을 검증한다. 할인·VIP·입력 검증은 이 계약 범위 밖이다.

### 1.2 전제 조건

- `items`는 dict 리스트이며, 각 dict는 최소 `price`(int), `qty`(int) 키를 가진다.
- `sku` 등 추가 필드는 계산에 영향을 주지 않는다.
- 테스트는 `@pytest.mark.entity` 마커를 사용한다.

### 1.3 테스트 케이스

| ID | 시나리오 | 입력 | 기대 결과 | RED 우선순위 |
|----|----------|------|-----------|--------------|
| TP-INV-1-01 | 단일 품목 | `[{"price": 10000, "qty": 2}]` | `20000` | 1 (가장 단순) |
| TP-INV-1-02 | Discovery 시나리오 | A×3(12,000) + B×1(30,000) | `66000` | 2 |
| TP-INV-1-03 | 복수 품목 합산 | `[{"price": 5000, "qty": 1}, {"price": 3000, "qty": 4}]` | `17000` | 3 |

**TP-INV-1-02 상세 입력**

```python
item_a = {"sku": "A", "price": 12000, "qty": 3}
item_b = {"sku": "B", "price": 30000, "qty": 1}
# subtotal([item_a, item_b]) == 66000
```

### 1.4 테스트 구현 가이드 (RED)

```python
"""INV-1: subtotal(items) == Σ(price × qty)"""

import pytest
from src.cart import subtotal

pytestmark = pytest.mark.entity


def test_inv_1_01_single_item_subtotal_equals_price_times_qty():
    """INV-1: 단일 품목 소계는 price × qty와 같다."""
    ...


def test_inv_1_02_discovery_scenario_subtotal_equals_66000():
    """INV-1: Discovery 시나리오(A×3 + B×1) 소계는 66,000원이다."""
    ...


def test_inv_1_03_multiple_items_subtotal_equals_sum_of_price_times_qty():
    """INV-1: 복수 품목 소계는 각 price × qty의 합과 같다."""
    ...
```

### 1.5 GREEN 최소 구현

- `items`를 순회하며 `price * qty`를 누적 합산한다.
- 합산 줄에 `# INV-1` 주석을 단다.

### 1.6 범위 외

| 항목 | 이유 |
|------|------|
| `items is None` | E-1 |
| 음수 `price` / `qty` | E-2 |
| 빈 리스트 `[]`, `qty == 0` | README 계약 ID에 없음 |
| 문턱·VIP 할인 | INV-2 ~ INV-4 |

---

## 2. E-1 — items None

### 2.1 목적

`items`가 `None`일 때 소계 계산이 진행되지 않고 **`TypeError`** 가 발생함을 검증한다. `None`을 빈 장바구니(0원)로 처리하는 동작은 금지된다.

### 2.2 전제 조건

- E-1은 **입력 검증** 계약이다. 소계 값(INV-1)은 검증하지 않는다.
- 예외 타입은 **`TypeError`** (`ValueError` 아님).
- 테스트는 `@pytest.mark.boundary` 마커를 사용한다.
- INV-1 RED/GREEN이 선행되어 `subtotal()` 함수가 존재해야 한다.

### 2.3 테스트 케이스

| ID | 시나리오 | 입력 | 기대 결과 | RED 우선순위 |
|----|----------|------|-----------|--------------|
| TP-E-1-01 | None 전달 | `subtotal(None)` | `TypeError` 발생 | 1 |

```python
with pytest.raises(TypeError):
    subtotal(None)
```

- 반환값이 `0`이거나 조용히 통과하면 **실패**.
- `ValueError`만 발생하면 README 계약 불일치로 **실패**.

### 2.4 테스트 구현 가이드 (RED)

```python
"""E-1: items is None → TypeError"""

import pytest
from src.cart import subtotal

pytestmark = pytest.mark.boundary


def test_e_1_01_none_items_raises_type_error():
    """E-1: items가 None이면 TypeError를 발생시킨다."""
    with pytest.raises(TypeError):
        subtotal(None)
```

### 2.5 GREEN 최소 구현

```python
def subtotal(items):
    if items is None:  # E-1
        raise TypeError("items must not be None")
    ...
```

### 2.6 범위 외

| 항목 | 이유 |
|------|------|
| `items == []` (빈 리스트) | README E-1/E-2에 없음 |
| HTTP 4xx 응답 | Flask Boundary·별도 E-* (본 실습 범위 밖) |
| 음수 `price` / `qty` | E-2 |
| 정상 소계 값 | INV-1 |

---

## 3. E-2 — 음수 price 또는 qty

### 3.1 목적

품목의 `price` 또는 `qty`가 음수일 때, **문제 품목의 인덱스**를 담은 `ValueError`가 발생함을 검증한다. CS 사례(수량 -1 → 화면 0원)처럼 조용히 0원으로 처리되는 동작은 금지된다.

### 3.2 전제 조건

- E-2는 **입력 검증** 계약이다. 정상 입력의 소계(INV-1)는 별도 검증한다.
- 예외 타입은 **`ValueError`** 이다.
- 오류 메시지에 **해당 품목의 리스트 인덱스**가 포함되어야 한다.
- 테스트는 `@pytest.mark.boundary` 마커를 사용한다.
- INV-1, E-1 RED/GREEN이 선행되어 `subtotal()` 진입·순회 구조가 있어야 한다.

### 3.3 테스트 케이스

| ID | 시나리오 | 입력 | 기대 결과 | RED 우선순위 |
|----|----------|------|-----------|--------------|
| TP-E-2-01 | 음수 qty (index 0) | `[{"price": 1000, "qty": -1}]` | `ValueError`, 메시지에 `0` | 1 |
| TP-E-2-02 | 음수 price (index 0) | `[{"price": -500, "qty": 1}]` | `ValueError`, 메시지에 `0` | 2 |
| TP-E-2-03 | 두 번째 품목 음수 qty | `[{"price": 1000, "qty": 1}, {"price": 2000, "qty": -3}]` | `ValueError`, 메시지에 `1` | 3 |

**공통 assertion 패턴**

```python
with pytest.raises(ValueError, match=r"index\s+0"):
    subtotal([{"price": 1000, "qty": -1}])
```

### 3.4 테스트 구현 가이드 (RED)

```python
"""E-2: price 또는 qty가 음수 → ValueError, 인덱스 포함"""

import pytest
from src.cart import subtotal

pytestmark = pytest.mark.boundary


def test_e_2_01_negative_qty_at_index_zero_raises_value_error_with_index():
    """E-2: qty가 음수이면 인덱스를 포함한 ValueError를 발생시킨다."""
    ...


def test_e_2_02_negative_price_at_index_zero_raises_value_error_with_index():
    """E-2: price가 음수이면 인덱스를 포함한 ValueError를 발생시킨다."""
    ...


def test_e_2_03_negative_qty_at_later_index_raises_value_error_with_index():
    """E-2: 두 번째 품목 qty가 음수이면 해당 인덱스가 오류에 포함된다."""
    ...
```

### 3.5 GREEN 최소 구현

```python
for index, item in enumerate(items):
    price = item["price"]
    qty = item["qty"]
    if price < 0 or qty < 0:  # E-2
        raise ValueError(f"negative price or qty at index {index}")
    total += price * qty  # INV-1
```

### 3.6 범위 외

| 항목 | 이유 |
|------|------|
| `price == 0` 또는 `qty == 0` | README 계약 ID에 없음 |
| `qty`가 float·문자열 등 비정수 | README 계약 ID에 없음 |
| `items is None` | E-1 (`TypeError`) |
| 빈 리스트 `[]` | README 계약 ID에 없음 |
| HTTP 폼 오류 응답 | Flask Boundary·별도 계약 (본 실습 범위 밖) |

---

## 4. 전체 완료 기준

### INV-1

- [ ] TP-INV-1-01 ~ 03 RED에서 실패 → GREEN 후 통과
- [ ] 구현 줄에 `# INV-1` 주석

### E-1

- [ ] TP-E-1-01 RED에서 실패 → GREEN 후 통과
- [ ] 구현 줄에 `# E-1` 주석

### E-2

- [ ] TP-E-2-01 ~ 03 RED에서 실패 → GREEN 후 통과
- [ ] 각 케이스에서 `ValueError`와 **정확한 인덱스** 확인
- [ ] 구현 줄에 `# E-2` 주석

---

## 5. 실행 명령

```bash
# 계약별
pytest tests/entity/test_inv_1_subtotal.py -q
pytest tests/boundary/test_e_1_items_none.py -q
pytest tests/boundary/test_e_2_negative_price_or_qty.py -q

# 본 테스트 플랜 전체 (해당 파일 존재 시)
pytest tests/entity/test_inv_1_subtotal.py tests/boundary/test_e_1_items_none.py tests/boundary/test_e_2_negative_price_or_qty.py -q
```
