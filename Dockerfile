# ────────────────────────────────────────────────
# Stage 1: Builder — 安裝依賴套件
# ────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# 只複製依賴描述檔，善用 Docker layer cache
COPY requirements.txt pyproject.toml ./
COPY src/ ./src/

# 升級 pip 並安裝到指定目錄（不汙染系統）
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && pip install --no-cache-dir --prefix=/install -e .

# ────────────────────────────────────────────────
# Stage 2: Runtime — 最終映像（輕量）
# ────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# 安全：以非 root 使用者執行
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# 從 builder 複製已安裝的套件
COPY --from=builder /install /usr/local

# 複製應用程式原始碼
COPY --from=builder /build/src ./src

# 確保 Python 能找到 src 目錄下的模組
ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# 切換至非 root 使用者
USER appuser

# 暴露 Flask 使用的連接埠
EXPOSE 19191

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:19191/')" || exit 1

# 啟動指令：使用 Python 模組方式執行
CMD ["python", "-m", "project1.main"]
