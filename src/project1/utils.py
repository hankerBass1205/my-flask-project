"""輔助工具函式模組。"""

import threading
import time


def multiply(a: int, b: int) -> int:
    """計算兩個整數的乘積。"""
    return a * b


def capitalize_words(text: str) -> str:
    """將字串中每個單字的首字母轉為大寫。"""
    return " ".join(word.capitalize() for word in text.split())


# ── Feature 4：CPU 燒機工具 ────────────────────────────────────────────────

# 全域狀態，供路由查詢目前燒機狀態
_stress_lock = threading.Lock()
_stress_status: dict = {"running": False, "started_at": None, "duration": 0}


def cpu_stress_worker(duration: int = 30) -> None:
    """在背景執行緒中持續進行 CPU 密集運算，使 CPU 使用率提升至 60% 以上。

    採用「計算 + 短暫休眠」交替策略：
    - 每個週期內執行 0.8 秒的純數學運算（佔用 CPU）
    - 接著休眠 0.2 秒（讓 OS 排程器有機會回報使用率）
    - 整體 CPU 使用率約落在 70–90%，遠超 60% 門檻

    Args:
        duration: 燒機持續秒數，預設 30 秒。
    """
    with _stress_lock:
        _stress_status["running"] = True
        _stress_status["started_at"] = time.time()
        _stress_status["duration"] = duration

    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            # 0.8 秒的 CPU 密集計算
            cycle_end = time.time() + 0.8
            x = 0.0
            while time.time() < cycle_end:
                # 純數學運算，不涉及 I/O，確保 CPU 持續忙碌
                x = (x + 1.0) ** 0.5 * 3.14159
            # 短暫讓出 CPU，讓 OS 能正確統計使用率
            time.sleep(0.2)
    finally:
        with _stress_lock:
            _stress_status["running"] = False


def start_cpu_stress(duration: int = 30) -> dict:
    """啟動 CPU 燒機背景執行緒。

    若燒機已在執行中，直接回傳目前狀態而不重複啟動。

    Args:
        duration: 燒機持續秒數，預設 30 秒。

    Returns:
        dict: 包含 started（是否新啟動）與 status 的結果字典。
    """
    with _stress_lock:
        if _stress_status["running"]:
            return {"started": False, "message": "燒機已在執行中", "status": _stress_status.copy()}

    thread = threading.Thread(
        target=cpu_stress_worker,
        args=(duration,),
        daemon=True,  # 主程式結束時自動終止，不阻塞容器關閉
        name="cpu-stress-worker",
    )
    thread.start()
    return {"started": True, "message": f"CPU 燒機已啟動，持續 {duration} 秒", "status": _stress_status.copy()}


def get_stress_status() -> dict:
    """取得目前燒機狀態的快照。"""
    with _stress_lock:
        return _stress_status.copy()

