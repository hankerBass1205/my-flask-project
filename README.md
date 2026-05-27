# Python 專案 (project1)

這是一個標準且現代化的 Python 3.12 專案架構。本專案採用了業界推薦的 **`src/` layout**，使用 PEP 621 標準 `pyproject.toml` 進行專案與工具設定，並導入了超高速 Rust 工具 `Ruff` 作為程式碼品質檢查與格式化工具，並以 `pytest` 進行單元測試。

---

## 專案目錄結構

```text
project1/
├── .venv/                  # Python 虛擬環境 (Git 自動忽略)
├── .vscode/                # VS Code 專案專屬設定
│   └── settings.json       # 整合開發體驗設定 (Ruff + pytest + 自動格式化)
├── src/                    # 原始碼主目錄
│   └── project1/           # 專案套件主目錄
│       ├── __init__.py     # 模組初始化標記與版本定義
│       ├── main.py         # 應用程式進入點與核心邏輯
│       └── utils.py        # 輔助工具函式
├── test/                   # 單元測試目錄
│   ├── __init__.py         # 測試套件初始化標記
│   └── test_main.py        # pytest 單元測試案例
├── .editorconfig           # 跨編輯器程式碼格式規範設定
├── .gitignore              # Git 忽略檔案設定
├── pyproject.toml          # 現代 Python 專案的核心設定檔 (PEP 621)
├── requirements.txt        # 開發與生產依賴定義
└── README.md               # 專案說明文件 (本檔案)
```

---

## 開發指南

### 1. 建立並啟動虛擬環境 (Virtual Environment)

在專案根目錄下執行以下命令：

**Windows (PowerShell):**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2. 安裝依賴套件

啟動虛擬環境後，升級 pip 並安裝開發套件（包含 `pytest` 與 `ruff`）：

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. 執行主程式

由於專案採用了標準的套件架構，建議在根目錄下使用模組化方式（`-m`）來執行主程式：

**Windows (PowerShell):**
*(Windows 控制台預設使用 CP950 編碼，若程式包含 Unicode 圖示，請先設定編碼為 UTF-8)*
```powershell
$env:PYTHONIOENCODING="utf-8"
$env:PYTHONPATH="src"
python -m project1.main
```

**macOS / Linux:**
```bash
PYTHONPATH=src python3 -m project1.main
```

---

### 4. 執行單元測試

專案配置了 `pyproject.toml` 中的 `pytest` 路徑設定，可直接在專案根目錄執行測試，無需設定複雜的搜尋路徑：

```powershell
pytest
```

---

### 5. 程式碼品質與格式化 (Ruff)

本專案使用極速的 `Ruff` 進行程式碼品質檢查與自動格式化：

* **執行程式碼風格檢查 (Linter):**
  ```powershell
  ruff check src test
  ```
  *(可加入 `--fix` 自動修復可修正的警告：`ruff check src test --fix`)*

* **執行自動格式化 (Formatter):**
  ```powershell
  ruff format src test
  ```

---

## VS Code 整合開發體驗

為確保最佳開發體驗，專案中已預先配置好 `.vscode/settings.json`：
1. **自動解譯器選取：** 開啟專案時，VS Code 將自動指定專案內的 `.venv` 為 Python 執行環境。
2. **存檔自動排版與優化：** 只要在存檔時，VS Code 就會呼叫 `Ruff` 自動為您的 Python 程式碼進行**格式排版**、**排序匯入 (import sorting)** 與**自動修正 Linter 警告**。
3. **建議安裝套件：**
   * [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) - 官方 Python 支援套件。
   * [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) - 官方極速 Ruff Linter / Formatter。
