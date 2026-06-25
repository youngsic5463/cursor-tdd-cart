"""E-1, E-2: subtotal() 입력 검증 계약 · UC-1, UC-2, UE-1: Flask 주문 폼 계약"""

import pytest

from src.app import app
from src.cart import subtotal

pytestmark = pytest.mark.boundary


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_e_1_none_items_raises_type_error():
    """E-1: subtotal(None)은 TypeError를 던진다."""
    with pytest.raises(TypeError):
        subtotal(None)


def test_e_2_negative_qty_raises_value_error_with_index():
    """E-2: 음수 qty는 ValueError를 던지고 메시지에 인덱스가 포함된다."""
    with pytest.raises(ValueError, match=r"index\s+0"):
        subtotal([{"price": 1000, "qty": -1}])


def test_e_2_negative_price_raises_value_error_with_index():
    """E-2: 음수 price는 ValueError를 던지고 메시지에 인덱스가 포함된다."""
    with pytest.raises(ValueError, match=r"index\s+0"):
        subtotal([{"price": -500, "qty": 1}])


def test_uc_1_get_root_returns_form_with_qty_input(client):
    """UC-1: GET / 는 200을 반환하고 본문에 name=\"qty\" 입력이 있다."""
    response = client.get("/")

    assert response.status_code == 200
    assert 'name="qty"' in response.get_data(as_text=True)


def test_uc_2_post_calc_shows_final_total(client):
    """UC-2: POST /calc (price·qty·vip) 는 본문에 final_total 결과를 표시한다."""
    response = client.post(
        "/calc",
        data={"price": 60000, "qty": 1, "vip": "on"},
    )

    assert "51300" in response.get_data(as_text=True)


def test_ue_1_non_numeric_qty_returns_400(client):
    """UE-1: qty 가 숫자가 아니면 400을 반환한다."""
    response = client.post(
        "/calc",
        data={"price": 60000, "qty": "abc"},
    )

    assert response.status_code == 400
