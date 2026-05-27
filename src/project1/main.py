from project1.utils import capitalize_words, multiply


def add(a: int, b: int) -> int:
    """計算兩個整數的和。"""
    return a + b


def greet(name: str) -> str:
    """產生問候語。"""
    return f"Hello, {name}!"


def run_cli_demo() -> None:
    """終端機展示邏輯。"""
    print("\n" + "=" * 35)
    print("🚀 Python CLI 測試範例")
    print("=" * 35)
    a, b = 5, 7
    print(f"🔹 基礎運算: {a} + {b} = {add(a, b)}")
    print(f"🔹 乘法運算: {a} * {b} = {multiply(a, b)}")
    print(f"🔹 問候測試: {greet(capitalize_words('developer workspace'))}")
    print("=" * 35 + "\n")


def main() -> None:
    """主程式進入點，啟動 Flask Web 伺服器並綁定至連接埠 19191。"""
    from project1.app import create_app

    app = create_app()

    port = 19191

    print("\n" + "=" * 55)
    print("🚀 Flask Web 應用程式啟動中...")
    print(f"🌐 本地伺服器位址: http://127.0.0.1:{port}")
    print(f"🔒 部署連接埠: {port}")
    print("=" * 55 + "\n")

    # 啟動 Flask，設定 host='0.0.0.0' 以允許外部訪問，並綁定 19191
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
