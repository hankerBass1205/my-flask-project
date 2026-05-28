# 🐳 Docker 部署指南 — project1 Flask 應用程式

## 📁 新增的 Docker 相關檔案

```
project1/
├── Dockerfile          # 多階段建置映像定義
├── docker-compose.yml  # 服務編排設定
└── .dockerignore       # 排除不需要的檔案
```

---

## 🚀 快速啟動

### 前置需求
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 已安裝並執行中

### 方式一：使用 Docker Compose（推薦）

```bash
# 建置並啟動
docker-compose up --build

# 背景執行
docker-compose up --build -d

# 停止服務
docker-compose down
```

### 方式二：直接使用 Docker

```bash
# 建置映像
docker build -t project1:latest .

# 執行容器
docker run -d -p 19191:19191 --name project1_web project1:latest

# 停止並移除容器
docker stop project1_web && docker rm project1_web
```

---

## 🌐 服務位址

| 服務 | URL |
|------|-----|
| Web 首頁 | http://localhost:19191/ |
| 功能一 | http://localhost:19191/feat1 |
| 功能二 | http://localhost:19191/feat2 |
| 計算 API | http://localhost:19191/api/calculate |

---

## 🔧 常用管理指令

```bash
# 查看執行中容器
docker ps

# 查看應用程式日誌
docker-compose logs -f web

# 進入容器 shell（除錯用）
docker exec -it project1_web bash

# 查看容器健康狀態
docker inspect --format='{{.State.Health.Status}}' project1_web

# 重建映像（程式碼更新後）
docker-compose up --build -d
```

---

## 📡 API 測試範例

```bash
# 加法運算
curl -X POST http://localhost:19191/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"action": "add", "a": 5, "b": 7}'

# 乘法運算
curl -X POST http://localhost:19191/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"action": "multiply", "a": 5, "b": 7}'

# 問候語
curl -X POST http://localhost:19191/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"action": "greet", "name": "Developer"}'
```

---

## 🏗️ Dockerfile 架構說明

採用 **多階段建置（Multi-stage Build）** 策略：

| 階段 | 用途 |
|------|------|
| `builder` | 安裝所有 Python 套件，編譯依賴 |
| `runtime` | 只複製必要檔案，映像更輕量安全 |

### 安全特性
- ✅ 以非 root 使用者（`appuser`）執行
- ✅ 內建 Health Check（每 30 秒檢查一次）
- ✅ `PYTHONDONTWRITEBYTECODE=1` 避免產生 `.pyc` 檔案

---

## ☁️ AWS 部署提示

若要部署至 AWS，可考慮：

1. **Amazon ECR** — 推送 Docker 映像
   ```bash
   # 登入 ECR
   aws ecr get-login-password --region ap-northeast-1 | \
     docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.ap-northeast-1.amazonaws.com

   # 標記並推送
   docker tag project1:latest <your-account-id>.dkr.ecr.ap-northeast-1.amazonaws.com/project1:latest
   docker push <your-account-id>.dkr.ecr.ap-northeast-1.amazonaws.com/project1:latest
   ```

2. **Amazon ECS / Fargate** — 無伺服器容器執行
3. **Amazon EC2** — 在 EC2 上直接執行 Docker Compose
