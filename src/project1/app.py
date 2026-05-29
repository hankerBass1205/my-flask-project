"""Flask Web 應用程式工廠模組。"""

import logging
from typing import Any

import boto3
import botocore.exceptions
from flask import Flask, jsonify, render_template, request

from project1.main import add, greet
from project1.utils import capitalize_words, multiply, start_cpu_stress, get_stress_status

# 模組層級 Logger，異常訊息會同時寫入 Flask/Gunicorn 日誌
logger = logging.getLogger(__name__)

# AWS S3 配置常數（不含任何金鑰）
S3_BUCKET = "hankdev-tw-storage-2026"
S3_REGION = "ap-east-2"


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

    @app.route("/feature3", methods=["GET", "POST"])
    def feature3() -> str:
        """功能三：將使用者上傳的檔案串接至 AWS S3 Bucket。

        GET  → 渲染上傳表單頁面。
        POST → 接收檔案，透過 boto3 上傳至 S3，回傳結果訊息。

        憑證讀取順序（boto3 預設鏈）：
          1. 環境變數 (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY)
          2. ~/.aws/credentials（本地開發）
          3. EC2 Instance Profile / IAM Role（雲端部署）
        """
        upload_result: dict[str, str] | None = None

        if request.method == "POST":
            file = request.files.get("file")

            if not file or file.filename == "":
                upload_result = {
                    "status": "error",
                    "message": "未選取任何檔案，請重新選擇後再上傳。",
                    "detail": "",
                    "filename": "",
                    "s3_key": "",
                }
            else:
                filename: str = file.filename  # type: ignore[assignment]
                s3_key = filename  # 直接以原始檔名作為 S3 Object Key

                try:
                    # 不傳入任何金鑰參數，boto3 自動套用憑證鏈
                    s3_client = boto3.client("s3", region_name=S3_REGION)
                    s3_client.upload_fileobj(file, S3_BUCKET, s3_key)

                    logger.info("S3 上傳成功：%s → s3://%s/%s", filename, S3_BUCKET, s3_key)
                    upload_result = {
                        "status": "success",
                        "message": "上傳成功",
                        "filename": filename,
                        "s3_key": s3_key,
                        "detail": "",
                    }

                except botocore.exceptions.NoCredentialsError as e:
                    detail = str(e)
                    logger.error("S3 上傳失敗（憑證未設定）：%s", detail)
                    upload_result = {
                        "status": "error",
                        "message": "找不到 AWS 憑證。請確認 ~/.aws/credentials 已設定，或 EC2 已綁定 IAM Role。",
                        "detail": detail,
                        "filename": filename,
                        "s3_key": "",
                    }

                except botocore.exceptions.ClientError as e:
                    detail = str(e)
                    logger.error("S3 上傳失敗（ClientError）：%s", detail)
                    upload_result = {
                        "status": "error",
                        "message": "S3 操作失敗，可能是 Bucket 名稱錯誤或 IAM 權限不足。",
                        "detail": detail,
                        "filename": filename,
                        "s3_key": "",
                    }

                except Exception as e:  # noqa: BLE001
                    detail = str(e)
                    logger.exception("S3 上傳發生非預期錯誤：%s", detail)
                    upload_result = {
                        "status": "error",
                        "message": "伺服器發生非預期錯誤，請查閱後端 Log。",
                        "detail": detail,
                        "filename": filename,
                        "s3_key": "",
                    }

        return render_template("feature3.html", upload_result=upload_result)

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

    # ── Feature 4：CPU 燒機 ────────────────────────────────────────────────

    @app.route("/feature4")
    def feature4() -> str:
        """功能四：CPU 燒機測試頁面。

        GET → 渲染燒機控制頁面，顯示目前燒機狀態。
        """
        status = get_stress_status()
        return render_template("feature4.html", stress_status=status)

    @app.route("/api/stress/start", methods=["POST"])
    def stress_start() -> tuple[Any, int]:
        """觸發 CPU 燒機 API。

        接收 JSON：{ "duration": 30 }（duration 可選，預設 30 秒）
        燒機邏輯在背景執行緒執行，不阻塞 Flask 主執行緒。
        """
        data: dict[str, Any] = request.get_json() or {}
        try:
            duration = int(data.get("duration", 30))
            if duration <= 0 or duration > 300:
                return jsonify({"status": "error", "message": "duration 必須介於 1–300 秒之間"}), 400
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "duration 參數格式錯誤"}), 400

        result = start_cpu_stress(duration=duration)
        http_status = 200 if result["started"] else 409  # 409 Conflict = 已在執行中
        logger.info("CPU 燒機請求：%s", result["message"])
        return jsonify({
            "status": "success",
            "started": result["started"],
            "message": result["message"],
            "stress": result["status"],
        }), http_status

    @app.route("/api/stress/status", methods=["GET"])
    def stress_status_api() -> tuple[Any, int]:
        """查詢目前 CPU 燒機狀態。"""
        return jsonify({"status": "success", "stress": get_stress_status()}), 200

    return app


