"""單元測試與 Flask 整合測試模組。"""

import pytest

from project1.app import create_app
from project1.main import add, greet
from project1.utils import capitalize_words, multiply


@pytest.fixture
def client():
    """建立 Flask 測試客戶端。"""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ==========================================================================
# 基礎函數單元測試
# ==========================================================================


def test_add():
    """測試 add 函數。"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_greet():
    """測試 greet 函數。"""
    assert greet("World") == "Hello, World!"
    assert greet("Python") == "Hello, Python!"


def test_multiply():
    """測試 utils.multiply 函數。"""
    assert multiply(3, 4) == 12
    assert multiply(-2, 5) == -10
    assert multiply(0, 100) == 0


def test_capitalize_words():
    """測試 utils.capitalize_words 函數。"""
    assert capitalize_words("hello world") == "Hello World"
    assert capitalize_words("python is awesome") == "Python Is Awesome"
    assert capitalize_words("") == ""


# ==========================================================================
# Flask Web 與 API 整合測試
# ==========================================================================


def test_index_route(client):
    """測試首頁路由渲染。"""
    response = client.get("/")
    assert response.status_code == 200
    html_content = response.data.decode("utf-8")
    assert "Flask Dashboard" in html_content
    assert "Port 19191" in html_content


def test_feat1_route(client):
    """測試 /feat1 路由。"""
    response = client.get("/feat1")
    assert response.status_code == 200
    content = response.data.decode("utf-8")
    assert content == "早上看股票"


def test_feat2_route(client):
    """測試 /feat2 路由。"""
    response = client.get("/feat2")
    assert response.status_code == 200
    content = response.data.decode("utf-8")
    assert content == "找下午上班的公司"


def test_api_calculate_add(client):
    """測試 API 的加法運算。"""
    response = client.post("/api/calculate", json={"action": "add", "a": 12, "b": 25})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["result"] == 37
    assert data["formula"] == "12 + 25 = 37"


def test_api_calculate_multiply(client):
    """測試 API 的乘法運算。"""
    response = client.post(
        "/api/calculate", json={"action": "multiply", "a": 5, "b": 7}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["result"] == 35


def test_api_calculate_greet(client):
    """測試 API 的問候運算。"""
    response = client.post(
        "/api/calculate", json={"action": "greet", "name": "Flask Developer"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["result"] == "Hello, Flask Developer!"


def test_api_calculate_capitalize(client):
    """測試 API 的首字大寫運算。"""
    response = client.post(
        "/api/calculate",
        json={"action": "capitalize", "text": "unit testing python app"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["result"] == "Unit Testing Python App"


def test_api_calculate_errors(client):
    """測試 API 的各種錯誤與邊界情況。"""
    # 測試缺少 action 參數
    response = client.post("/api/calculate", json={"a": 1})
    assert response.status_code == 400
    assert "未提供運算動作" in response.get_json()["message"]

    # 測試未知的 action 參數
    response = client.post(
        "/api/calculate", json={"action": "subtract", "a": 1, "b": 2}
    )
    assert response.status_code == 400
    assert "未知的運算動作" in response.get_json()["message"]

    # 測試加法參數格式錯誤（傳入字串無法轉成整數）
    response = client.post(
        "/api/calculate", json={"action": "add", "a": "hello", "b": 2}
    )
    assert response.status_code == 400
    assert "參數格式錯誤" in response.get_json()["message"]

    # 測試問候名字為空
    response = client.post("/api/calculate", json={"action": "greet", "name": ""})
    assert response.status_code == 400
    assert "請輸入名字" in response.get_json()["message"]
