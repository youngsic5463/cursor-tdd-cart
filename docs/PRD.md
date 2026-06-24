# PRD — 장바구니 할인 계산기 (cursor-tdd-cart)

| 항목 | 내용 |
|------|------|
| 프로젝트 | cursor-tdd-cart |
| 버전 | 0.1 (Discovery) |
| 작성일 | 2026-06-24 |
| 근거 문서 | [Report/02.REPORT.md](../Report/02.REPORT.md), [Prompting/02.Export-Transcript.md](../Prompting/02.Export-Transcript.md) |
| 개발 방식 | Dual-Track TDD (RED → GREEN → REFACTOR), 계약 ID 추적 |

---

## 1. 제품 개요

### 1.1 목적

장바구니 주문의 **소계 계산**과 **할인 규칙 적용**을 정확히 수행하는 계산기를 만든다. Flask 주문 폼(Boundary)과 순수 도메인 로직(Entity)을 분리하고, 모든 동작은 **테스트 가능한 계약 ID**로 추적한다.

### 1.2 범위

| 포함 | 제외 (OOS) |
|------|------------|
| 품목별 소계 계산 | 쿠폰 할인 |
| 5만 원 초과 시 10% 문턱 할인 | 배송비 |
| VIP 고객 5% 추가 할인 (문턱 후) | 세금·포인트·등급 확장 |
| 잘못된 입력 거부 (음수 수량, 빈 장바구니) | `subtotal == 50,000` 문턱 포함 여부 (미확인) |

### 1.3 아키텍처 (ECB)

| 계층 | 경로 | 역할 |
|------|------|------|
| Entity | `src/cart.py` | 순수 로직·불변식. Flask import 금지 |
| Boundary | `src/app.py` | Flask 주문 폼. `cart.py` 재사용 |
| Entity 테스트 | `tests/entity/` | INV-*, AC-* 검증 |
| Boundary 테스트 | `tests/boundary/` | E-* 검증 |

---

## 2. Discovery 근거

MomTest 방식 Product Discovery 세션([Report/02](../Report/02.REPORT.md))에서 아래 근거만으로 계약을 확정했다. **근거 없는 동작은 구현하지 않는다.**

### 2.1 인터뷰 메모 (2024-03-12)

- A 3개(12,000원) + B 1개(30,000원) = **66,000원**
- 5만 원 **넘으면** 10% 할인 → 기대 **59,400원**
- VIP 고객: 문턱 할인 후 추가 5% 할인. 순서 **문턱 → VIP** 고정

### 2.2 실제 주문 사례

| 주문 | 소계 | 결제 | 할인 |
|------|------|------|------|
| #1107 | 60,000 | 54,000 | 10% |
| #1042 | 48,000 | 48,000 | 없음 |

### 2.3 엑셀 검산

- 66,000 × 0.9 = 59,400 (`ROUND`)
- VIP 추가: 59,400 × 0.95 = **56,430**

### 2.4 CS 클레임 / 버그

| 사례 | 현재 동작 | 기대 동작 |
|------|-----------|-----------|
| 수량 -1 입력 | 화면 합계 0원 표시 | 오류 또는 거부 |
| items 없이 제출 | 500 에러 | 4xx + 명확한 오류 |

### 2.5 미확인 항목

- **50,000원 정확히**: "넘으면"만 확인됨. 포함 여부 실사례 없음 → OOS-3
- **쿠폰·배송비**: 언급 없음 → OOS-1, OOS-2

---

## 3. 계약 원칙

1. 계약은 반드시 ID를 가진다 (`INV-*`, `E-*`, `AC-*`, `OOS-*`).
2. ID는 테스트와 구현을 연결하는 **추적의 못**이다.
3. **Invariant**: 어떤 입력에서도 깨지면 안 되는 규칙.
4. **AC (Acceptance Criteria)**: 사용자가 수용하는 기능 조건.
5. **Error Contract**: 잘못된 입력에 대한 오류 규칙.
6. **ID에 없는 동작은 구현하지 않는다.**

---

## 4. 확정 계약

### 4.1 불변식 (Invariant)

| ID | 계약 | 근거 레벨 | 구현 |
|----|------|-----------|------|
| INV-1 | `subtotal = Σ(unit_price × qty)` (유효한 품목만) | L1 | `cart.py` |
| INV-2 | `subtotal > 50000`이면 `round(subtotal × 0.9)` 반환 | L1 | `cart.py` |
| INV-3 | `subtotal ≤ 50000`이면 문턱 할인 없이 `subtotal` 그대로 반환 | L1 | `cart.py` |
| INV-4 | `is_vip=True`이면 `round(after_threshold × 0.95)` 반환 | L2 | `cart.py` |
| INV-5 | `is_vip=False`이면 VIP 할인 없이 문턱 적용 후 금액 반환 | L2 | `cart.py` |
| INV-6 | 할인 적용 순서는 항상 **문턱 → VIP** | L2 | `cart.py` |
| INV-7 | 최종 결제액은 **0 이상의 정수(원)** | L3 | `cart.py` |
| INV-8 | 최종 결제액은 **항상 `subtotal` 이하** | L3 | `cart.py` |

### 4.2 에러 계약 (Error Contract)

| ID | 계약 | 근거 레벨 | 구현 |
|----|------|-----------|------|
| E-1 | `qty < 0`이면 인덱스를 포함한 `ValueError` 발생 (0원 표시 금지) | L0 | `cart.py` |
| E-2 | `items`가 `None`이거나 빈 리스트이면 `ValueError` 발생 | L0 | `cart.py` |
| E-3 | 빈/누락 `items` HTTP 제출 시 **4xx** 응답 (500 아님) | L0 | `app.py` |
| E-4 | `qty < 0` 제출 시 오류 응답 또는 오류 메시지 (합계 0원 표시 금지) | L0 | `app.py` |

### 4.3 수용 기준 (Acceptance Criteria)

| ID | 시나리오 | 입력 | 기대 결과 |
|----|----------|------|-----------|
| AC-1 | 주문 #1107 | 소계 60,000, non-VIP | 54,000 |
| AC-2 | 주문 #1042 | 소계 48,000, non-VIP | 48,000 |
| AC-3 | 인터뷰 시나리오 | A×3 + B×1, non-VIP | 59,400 |
| AC-4 | 인터뷰 VIP 시나리오 | A×3 + B×1, VIP | 56,430 |

### 4.4 테스트 가능 문장

```
INV-1:  calculate_subtotal([{sku:"A",qty:3,price:12000},{sku:"B",qty:1,price:30000}]) == 66000
INV-2:  apply_threshold(60000) == 54000; apply_threshold(66000) == 59400
INV-3:  apply_threshold(48000) == 48000
INV-4:  apply_vip(59400, is_vip=True) == 56430
INV-5:  apply_vip(59400, is_vip=False) == 59400
INV-6:  calculate_total(items, is_vip=True) == apply_vip(apply_threshold(subtotal), True)
INV-7:  ∀ valid input: isinstance(result, int) and result >= 0
INV-8:  ∀ valid input: result <= subtotal
E-1:    calculate_subtotal([{qty:-1,...}]) raises ValueError matching index
E-2:    calculate_subtotal(None) raises ValueError; calculate_subtotal([]) raises ValueError
E-3:    client.post("/", data={}) → status_code in (400, 422)
E-4:    client.post("/", data={qty:-1}) → not 200 with total=0
```

---

## 5. 범위 제외 (Out of Scope)

| OOS ID | 만들지 않을 동작 | 제외 이유 |
|--------|------------------|-----------|
| OOS-1 | 쿠폰 할인 | 근거 없음 |
| OOS-2 | 배송비 | 명시적 비범위 |
| OOS-3 | `subtotal == 50000`일 때 10% 할인 | "넘으면"만 확인; 실사례 없음 |
| OOS-4 | 문턱 미달인데 VIP 5%만 적용 | VIP 예시는 문턱 적용 후에만 근거 |
| OOS-5 | `qty == 0` 처리 규칙 | 사례 없음 |
| OOS-6 | 음수 단가(`price < 0`) | 사례 없음 |
| OOS-7 | 비정수 수량 | 사례 없음 |
| OOS-8 | 세금·포인트·회원 등급 확장 | 근거 없음 |
| OOS-9 | 할인 순서 변경 (VIP → 문턱) | "문턱 → VIP 고정"만 확인 |
| OOS-10 | 소수 원 미반올림 중간값 유지 | `ROUND`·정수 원만 확인 |

---

## 6. 미해결 Discovery 질문

OOS-3 해소 및 추가 계약 발견을 위해 아래 MomTest 질문으로 실사례를 수집한다. ([Prompting/02](../Prompting/02.Export-Transcript.md) 전문 참조)

### 할인 문턱·금액

1. 소계가 5만 원 근처였던 주문 중, 할인 적용 여부를 따진 사례는?
2. 할인 금액이 1원이라도 어긋났던 CS 사례는?
3. 엑셀 검산과 시스템 결제액이 달랐던 적이 있는가?

### VIP 할인

4. VIP인데 문턱 할인이 안 붙은(또는 반대) 주문 클레임은?
5. VIP 할인만 기대하고 문턱 할인은 없었던 주문이 있었는가?

### 잘못된 입력

6. 수량 0, 빈칸, 문자, 소수 입력 시 실제로 어떤 일이 벌어졌는가?
7. 빈 장바구니 제출 시 500 외 다른 반응을 본 적이 있는가?
8. 수량 -1이 0원 표시 후 결제·재고까지 이어졌는가?

### 규칙 조합·손실

9. 할인 순서를 잘못 적용했다고 판단한 사례는?
10. 계산 오류로 인한 손실(과다 할인, 미할인 클레임) 사례는?
11. 절대 나오면 안 된다고 생각하는 결제 결과(음수, 할인 전보다 비쌈)를 본 적이 있는가?

---

## 7. 구현 계획 (TDD RED 순서)

| 순서 | 계약 | 내용 |
|------|------|------|
| 1 | INV-1, AC-3 | 소계 계산 (66,000) |
| 2 | INV-3, AC-2 | 할인 없음 (48,000) |
| 3 | INV-2, AC-1 | 문턱 10% (60,000) |
| 4 | INV-4, INV-5, INV-6, AC-4 | VIP 조합 |
| 5 | INV-7, INV-8 | 안전 불변식 |
| 6 | E-1, E-2 | Entity 입력 검증 |
| 7 | E-3, E-4 | Boundary HTTP 검증 |

**주의:** OOS-3(정확히 50,000원)은 MomTest 질문 1·2번 답변이 나올 때까지 RED 테스트에 포함하지 않는다.

### 워크플로

- **RED**: `tests/`만 수정. `src/` 건드리지 않음.
- **GREEN**: 최소 구현. 구현 줄에 계약 ID 주석.
- **REFACTOR**: 전부 통과 후 구조 정리. `pytest -q`로 동작 불변 확인.
- **커밋 분리**: test(RED) / feat(GREEN) / refactor. 메시지에 계약 ID 포함.

### 테스트 명령

```bash
pytest -q                  # 전체
pytest tests/entity -q     # Entity (INV-*, AC-*)
pytest tests/boundary -q   # Boundary (E-*)
```

---

## 8. 상품 카탈로그 (Discovery 근거)

인터뷰·검산에 등장한 품목. 추가 품목은 근거 없이 확장하지 않는다.

| SKU | 단가 (원) | 근거 |
|-----|-----------|------|
| A | 12,000 | 인터뷰 2024-03-12 |
| B | 30,000 | 인터뷰 2024-03-12 |

---

## 9. 참고 문서

| 문서 | 설명 |
|------|------|
| [Report/02.REPORT.md](../Report/02.REPORT.md) | MomTest 계약 발견 세션 요약 |
| [Prompting/02.Export-Transcript.md](../Prompting/02.Export-Transcript.md) | Discovery 대화 전문·계약표 원본 |
| [AGENTS.md](../AGENTS.md) | 저장소 구조·TDD 워크플로 |
| [Report/01.REPORT.md](../Report/01.REPORT.md) | Export 세션 01 |
| [Prompting/01.Export-Transcript.md](../Prompting/01.Export-Transcript.md) | Export Transcript 01 |

---

*본 문서는 docs/PRD.md — 장바구니 할인 계산기 Product Requirements Document (Discovery v0.1, 2026-06-24)입니다.*
