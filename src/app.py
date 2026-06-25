"""Flask Boundary — 주문 폼 (Discovery 4.1).

ECB 역할:
- Boundary: HTTP 입력·검증·응답. 할인 공식은 Entity에 위임한다.
- Entity: ``src.cart.final_total`` (Flask import 금지).

계약:
- UC-1: GET / → 200, 본문에 qty·price·VIP 입력 폼 포함
- UC-2: POST /calc (price·qty·vip) → 본문에 final_total 결과 표시
- UE-1: qty가 숫자가 아니면 400 + 에러 메시지

폼 필드 SSOT: ``price``, ``qty``, ``vip`` (checkbox), POST action ``/calc``.
"""

from flask import Flask, request

from src.cart import final_total

app = Flask(__name__)


@app.get("/")
def index():
    # UC-1: GET / 는 200을 반환하고 수량·가격·VIP 입력 폼을 포함한다
    return (
        '<form action="/calc" method="post">'
        '<input name="price" type="number">'
        '<input name="qty" type="number">'
        '<input name="vip" type="checkbox">'
        '<button type="submit">계산</button>'
        "</form>"
    )


@app.post("/calc")
def calc():
    try:
        qty = int(request.form["qty"])  # UE-1
    except ValueError:
        return "qty must be a number", 400  # UE-1

    price = int(request.form["price"])
    is_vip = request.form.get("vip") == "on"
    items = [{"price": price, "qty": qty}]
    total = final_total(items, is_vip=is_vip)  # UC-2
    return str(total)  # UC-2
