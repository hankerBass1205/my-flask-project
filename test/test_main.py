"""單元測試與 Flask 整合測試模組。"""

import pytest

from project1.app import create_app
from project1.main import add, greet
from project1.utils import capitalize_words, multiply, start_cpu_stress, get_stress_status


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


# ==========================================================================
# Feature 4：CPU 燒機測試
# ==========================================================================


def test_feature4_route(client):
    """測試 /feature4 路由回傳 200 並包含關鍵 HTML 內容。"""
    response = client.get("/feature4")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "CPU 燒機壓測" in html
    assert "開始燒機" in html


def test_stress_start_api(client):
    """測試 /api/stress/start 能正常觸發燒機並回傳 200。"""
    # 使用極短的 duration（1 秒）避免測試執行時間過長
    response = client.post("/api/stress/start", json={"duration": 1})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["started"] is True
    assert "燒機已啟動" in data["message"]


def test_stress_start_duplicate(client):
    """測試燒機執行中再次觸發應回傳 409 Conflict。"""
    # 先啟動一次（duration=2 秒，確保第二次請求時仍在執行）
    client.post("/api/stress/start", json={"duration": 2})
    # 立即再次觸發
    response = client.post("/api/stress/start", json={"duration": 2})
    assert response.status_code == 409
    data = response.get_json()
    assert data["status"] == "success"
    assert data["started"] is False


def test_stress_start_invalid_duration(client):
    """測試 duration 參數驗證。"""
    # duration 為 0
    response = client.post("/api/stress/start", json={"duration": 0})
    assert response.status_code == 400

    # duration 超過上限
    response = client.post("/api/stress/start", json={"duration": 999})
    assert response.status_code == 400

    # duration 為非數字
    response = client.post("/api/stress/start", json={"duration": "abc"})
    assert response.status_code == 400


def test_stress_status_api(client):
    """測試 /api/stress/status 能正常回傳狀態。"""
    response = client.get("/api/stress/status")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "stress" in data
    assert "running" in data["stress"]


def test_cpu_stress_worker_util():
    """測試 start_cpu_stress 工具函式能正常啟動背景執行緒。"""
    result = start_cpu_stress(duration=1)
    # 若燒機尚未執行，應成功啟動
    assert "started" in result
    assert "message" in result
    assert "status" in result


def test_get_stress_status_util():
    """測試 get_stress_status 回傳正確的狀態結構。"""
    status = get_stress_status()
    assert isinstance(status, dict)
    assert "running" in status
    assert isinstance(status["running"], bool)
