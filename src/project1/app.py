"""Flask Web 應用程式工廠模組。"""

from typing import Any

from flask import Flask, jsonify, render_template, request

from project1.main import add, greet
from project1.utils import capitalize_words, multiply


def create_app() -> Flask:
    """建立並配置 Flask 應用程式。"""
    # 預設以當前 package 路徑為基準載入 templates 與 static
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        """首頁路由，渲染儀表板。"""
        return render_template("index.html")

    @app.route("/feat1")
    def feat1() -> str:
        """功能一：早上看股票。"""
        return "早上看股票"

    @app.route("/feat2")
    def feat2() -> str:
        """功能二：找下午上班的公司。"""
        return "找下午上班的公司"

    @app.route("/api/calculate", methods=["POST"])
    def calculate() -> tuple[Any, int]:
        """計算 API 端點。

        接收 JSON 請求，例如：
        - { "action": "add", "a": 5, "b": 7 }
        - { "action": "multiply", "a": 5, "b": 7 }
        - { "action": "greet", "name": "Developer" }
        - { "action": "capitalize", "text": "hello world" }
        """
        data: dict[str, Any] = request.get_json() or {}
        action = data.get("action")

        if not action:
            return jsonify(
                {"status": "error", "message": "未提供運算動作 (action)"}
            ), 400

        try:
            if action == "add":
                a = int(data.get("a", 0))
                b = int(data.get("b", 0))
                result = add(a, b)
                return jsonify(
                    {
                        "status": "success",
                        "result": result,
                        "formula": f"{a} + {b} = {result}",
                    }
                ), 200

            elif action == "multiply":
                a = int(data.get("a", 0))
                b = int(data.get("b", 0))
                result = multiply(a, b)
                return jsonify(
                    {
                        "status": "success",
                        "result": result,
                        "formula": f"{a} * {b} = {result}",
                    }
                ), 200

            elif action == "greet":
                name = str(data.get("name", ""))
                if not name:
                    return jsonify({"status": "error", "message": "請輸入名字"}), 400
                result = greet(name)
                return jsonify({"status": "success", "result": result}), 200

            elif action == "capitalize":
                text = str(data.get("text", ""))
                result = capitalize_words(text)
                return jsonify(
                    {"status": "success", "result": result, "original": text}
                ), 200

            else:
                return jsonify(
                    {"status": "error", "message": f"未知的運算動作: {action}"}
                ), 400

        except (ValueError, TypeError) as e:
            return jsonify(
                {"status": "error", "message": f"參數格式錯誤: {str(e)}"}
            ), 400
        except Exception as e:
            return jsonify({"status": "error", "message": f"伺服器錯誤: {str(e)}"}), 500

    return app
