# Cart Discount TDD Practice

장바구니 할인 계산 로직을 TDD 방식으로 구현하는 연습 프로젝트입니다.

**버전: v0.1 (Discovery)** · 상세 요구사항·Discovery 근거는 [docs/PRD.md](docs/PRD.md)를 참조하세요.

**현재 단계: RED 준비** — 계약 ID별 실패 테스트 작성 전입니다. 구현(GREEN)은 아직 시작하지 않았습니다.

---

## 릴리스 노트 — v0.1 (Discovery)

MomTest Discovery로 장바구니 할인 계약(`INV-*`, `E-*`)을 확정하고, Dual-Track TDD 실습을 위한 문서·스캐폴딩을 마련한 Discovery 릴리스입니다.

### ✨ 기능

_(이번 버전에는 사용자-facing 기능 구현이 포함되지 않습니다.)_

### 🐛 버그 수정

_(해당 없음)_

### 🧹 기타

**MomTest Discovery & 계약 문서화**

- MomTest Product Discovery 세션 결과를 바탕으로 계약 ID(`INV-1` ~ `INV-4`, `E-1`, `E-2`)를 확정하고 README·PRD에 정리했습니다.
- [docs/PRD.md](docs/PRD.md) — 제품 요구사항, Discovery 근거, ECB 아키텍처, OOS(범위 제외) 항목
- Discovery 세션 보고서: [Report/02.REPORT.md](Report/02.REPORT.md)

**프로젝트 스캐폴딩**

- Python 3.12 + pytest 기반 프로젝트 구조 (`src/`, `tests/entity/`, `tests/boundary/`)
- [AGENTS.md](AGENTS.md) — Dual-Track TDD 워크플로·커밋 규칙
- `.cursor/rules/dual-track-tdd.mdc` — RED → GREEN → REFACTOR 작업 규칙

**세션 아카이브 & Cursor 도구**

- 대화 Transcript: [Prompting/02.Export-Transcript.md](Prompting/02.Export-Transcript.md)
- `/export` Cursor Command — 세션 보고서·Transcript 자동 생성

### 진행 상태

| 항목 | 상태 |
|------|------|
| Discovery / 계약 확정 | ✅ 완료 |
| RED (실패 테스트 작성) | 🔜 예정 |
| GREEN (최소 구현) | ⏸ 미시작 |

### 알려진 미확정 항목 (OOS)

- `subtotal == 50,000` 문턱 할인 **포함 여부** — "넘으면"만 확인됨, RED 전 추가 MomTest 인터뷰 필요
- 쿠폰, 배송비, 세금, 포인트 등 — 범위 제외

---

## 목적

이 프로젝트는 장바구니 할인 계산 로직을 **TDD(Test-Driven Development)** 로 구현하는 연습 프로젝트입니다.

도메인 로직은 `src/cart.py`의 Entity 계층에 위치합니다. 모든 동작은 **계약 ID**(`INV-*`, `E-*`)를 기준으로 테스트와 구현을 추적합니다. 계약 ID는 테스트와 구현을 잇는 **추적의 못**입니다.

---

## 핵심 원칙

1. **ID에 없는 동작은 만들지 않는다.** 계약 표에 없는 기능·예외·할인 정책은 구현하지 않습니다.
2. **테스트가 먼저다.** 구현보다 실패하는 테스트가 항상 앞섭니다.
3. **RED → GREEN → REFACTOR** 순서를 따릅니다.
   - RED: `tests/`만 수정. `src/`는 건드리지 않습니다.
   - GREEN: 해당 계약 ID를 만족하는 최소 구현만 작성합니다.
   - REFACTOR: 전부 통과한 뒤에만 구조를 개선합니다.
4. **과잉 구현을 금지한다.** 요청·계약에 없는 기능을 미리 만들지 않습니다.

---

## 계약 ID 목록

| ID    | 계약(불변식 / 에러)                                                 | 근거 레벨 | 계층        |
| ----- | ------------------------------------------------------------ | ----- | --------- |
| INV-1 | `subtotal(items) == Σ(price × qty)`                          | —     | Entity    |
| INV-2 | `amount ≥ 50000 → round(amount×0.9)` / `< 50000 → 그대로` 경계 포함 | L1    | Entity    |
| INV-3 | `final = 문턱할인 적용 후, VIP면 round(×0.95)`. 순서 문턱→VIP 고정         | L2    | Entity    |
| INV-4 | 모든 입력에서 `0 ≤ final_total ≤ subtotal`. 할인은 금액을 늘리지 않는다        | L3    | Entity    |
| E-1   | `items is None → TypeError`                                  | L0    | Boundary* |
| E-2   | `price` 또는 `qty`가 음수 → `ValueError`, 인덱스 포함                  | L0    | Boundary* |

---

## 계약 ID 설명

### INV-1 — 소계 계산

품목 목록 `items`의 소계는 각 품목의 `price × qty` 합과 같아야 합니다.

### INV-2 — 문턱 할인

금액이 50,000원 이상이면 `round(amount × 0.9)`를 적용하고, 50,000원 미만이면 원래 금액을 그대로 반환합니다. 경계값 50,000원은 할인에 포함됩니다.

### INV-3 — VIP 할인 및 적용 순서

문턱 할인을 먼저 적용한 뒤, VIP 고객이면 `round(× 0.95)`를 적용합니다. 적용 순서는 **문턱 → VIP**로 고정됩니다.

### INV-4 — 안전 불변식

유효한 모든 입력에서 최종 결제액 `final_total`은 0 이상이며 `subtotal` 이하여야 합니다. 할인으로 금액이 늘어나지 않습니다.

### E-1 — items None

`items`가 `None`이면 `TypeError`를 발생시킵니다.

### E-2 — 음수 price 또는 qty

`price` 또는 `qty`가 음수이면 인덱스를 포함한 `ValueError`를 발생시킵니다.

---

## 계층 의미

### Entity

`src/cart.py`에 위치하는 **순수 도메인 계산 로직** 계층입니다. Flask 등 외부 프레임워크를 import하지 않습니다. INV-1 ~ INV-4 불변식을 담당합니다.

### Boundary*

E-1, E-2는 입력 검증 경계에 가까운 규칙입니다. 본 실습에서는 Flask 폼 등 별도 Boundary 계층 없이 **도메인 함수 진입점**(`cart.py`)에서 검증합니다. 계층 표기의 `Boundary*`는 이 의미를 나타냅니다.

---

## 예상 파일 구조

```text
.
├── README.md
├── src/
│   └── cart.py
└── tests/
    └── test_cart.py
```

---

## TDD 진행 순서

| 단계 | 작업 |
|------|------|
| **RED** | 계약 ID별 실패 테스트 작성 (`tests/test_cart.py`) |
| **GREEN** | 해당 ID를 만족하는 최소 구현 (`src/cart.py`) |
| **REFACTOR** | 테스트 통과 상태에서 구조 개선 |

권장 RED 순서: INV-1 → INV-2 → INV-3 → INV-4 → E-1 → E-2

구현 시 해당 줄에 충족한 계약 ID를 주석으로 표기합니다.

---

## REFACTOR 계획 (Track B · subtotal)

Track B(E-1, E-2) GREEN 이후 `subtotal`의 **Mixed Responsibilities** 스멜을 해소하기 위한 구조 개선 계획입니다. 동작 변경 없이 E-2 검증만 private helper로 분리합니다.

### 목적

- E-2(`price` / `qty` 음수 검증)를 `_validate_line_items(items)`로 추출한다.
- E-1(`items is None → TypeError`)은 `subtotal` 진입부에 그대로 둔다.
- INV-1 합산 루프(`total += price * qty`)는 `subtotal`에 유지한다.

### 변경 범위

| 항목 | 내용 |
|------|------|
| 변경 파일 | `src/cart.py`만 |
| 테스트 | `tests/` 수정 없음 |
| 공개 API | `subtotal(items)` 시그니처·import 경로 불변 |

### 제외

- `sum()` 변환
- `"price"` / `"qty"` 상수 추출
- `apply_threshold_discount`, `final_total`, `THRESHOLD` 등 INV-2 이후 함수·상수

### 동작 불변 체크리스트

REFACTOR 전후 아래가 동일해야 합니다.

| 계약 | 확인 항목 |
|------|-----------|
| E-1 | `subtotal(None)` → `TypeError`, 메시지 `"items must not be None"` |
| E-2 | 음수 `price` / `qty` → `ValueError`, 메시지에 해당 **인덱스** 포함 (`index 0` 등) |
| INV-1 | `subtotal([{"price": 1000, "qty": 3}, {"price": 2000, "qty": 2}]) == 7000` |

### 완료 기준

- REFACTOR **전** `pytest -q` GREEN
- REFACTOR **후** `pytest -q` GREEN (동작 불변)

### 예상 diff

- `src/cart.py` **+3~5줄** (E-2 블록 추출 + `_validate_line_items(items)` 호출 1줄)

---

## 테스트 실행

```bash
pytest -q
```

`-q`는 quiet mode로, 테스트 결과를 간략하게 출력합니다.

---

## 구현 금지 사항

- 할인 정책 추가 금지
- 쿠폰, 세금, 배송비, 포인트 기능 추가 금지
- ID에 없는 예외 처리 추가 금지
- UI, CLI, DB, API 코드 추가 금지
