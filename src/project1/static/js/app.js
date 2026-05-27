/**
 * 前端應用程式控制邏輯
 * 實作非同步 API 串接與玻璃擬態動態互動特效
 */

document.addEventListener("DOMContentLoaded", () => {
    // 獲取 DOM 節點
    const actionSelect = document.getElementById("action-select");
    const inputsMath = document.getElementById("inputs-math");
    const inputsText = document.getElementById("inputs-text");
    const btnSubmit = document.getElementById("btn-submit");
    const btnLoader = document.getElementById("btn-loader");
    const consoleOutput = document.getElementById("console-output");
    const apiStatusText = document.getElementById("api-status-text");
    const pulseDot = document.querySelector(".pulse-dot");

    // 數值輸入項
    const numA = document.getElementById("num-a");
    const numB = document.getElementById("num-b");
    const textInput = document.getElementById("text-input");

    /**
     * 動態欄位切換邏輯
     */
    actionSelect.addEventListener("change", (e) => {
        const value = e.target.value;
        if (value === "add" || value === "multiply") {
            inputsMath.classList.remove("hidden");
            inputsText.classList.add("hidden");
        } else {
            inputsMath.classList.add("hidden");
            inputsText.classList.remove("hidden");
        }
        
        // 切換時清除舊的日誌
        consoleOutput.innerHTML = `<div class="console-placeholder">切換運算類型。已準備好發送 ${value} 請求...</div>`;
    });

    /**
     * 發送 API 計算請求
     */
    btnSubmit.addEventListener("click", async () => {
        const action = actionSelect.value;
        let requestData = { action: action };

        // 根據不同類型構建 payload
        if (action === "add" || action === "multiply") {
            const valA = parseInt(numA.value, 10);
            const valB = parseInt(numB.value, 10);

            if (isNaN(valA) || isNaN(valB)) {
                showError("請確保 A 與 B 輸入了有效的整數。");
                return;
            }
            requestData.a = valA;
            requestData.b = valB;
        } else if (action === "greet") {
            const nameVal = textInput.value.trim();
            if (!nameVal) {
                showError("問候名字欄位不能為空。");
                return;
            }
            requestData.name = nameVal;
        } else if (action === "capitalize") {
            const textVal = textInput.value.trim();
            requestData.text = textVal;
        }

        // 開啟 Loading 動態效果
        setLoading(true);

        try {
            const response = await fetch("/api/calculate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();

            if (response.ok && data.status === "success") {
                showSuccess(data);
            } else {
                showError(data.message || "發生未知錯誤");
            }
        } catch (error) {
            showError(`網路通訊失敗，無法連線至 API 伺服器:\n${error.message}`);
        } finally {
            setLoading(false);
        }
    });

    /**
     * Loading 狀態設定
     */
    function setLoading(isLoading) {
        if (isLoading) {
            btnSubmit.disabled = true;
            btnLoader.classList.remove("hidden");
            pulseDot.className = "pulse-dot loading";
            apiStatusText.textContent = "正在發送請求至後端 API...";
        } else {
            btnSubmit.disabled = false;
            btnLoader.classList.add("hidden");
        }
    }

    /**
     * 呈現成功回應日誌
     */
    function showSuccess(data) {
        pulseDot.className = "pulse-dot";
        apiStatusText.textContent = "運算完成，API 回應成功！";
        
        // 格式化 JSON 呈現
        const timestamp = new Date().toLocaleTimeString();
        let logHtml = `[${timestamp}] << API 回應 200 OK >>\n\n`;
        logHtml += JSON.stringify(data, null, 4);

        consoleOutput.innerHTML = `<span style="color: #a7f3d0;">${logHtml}</span>`;
    }

    /**
     * 呈現錯誤回應日誌
     */
    function showError(message) {
        pulseDot.className = "pulse-dot error";
        apiStatusText.textContent = "運算失敗，後端拒絕請求。";

        const timestamp = new Date().toLocaleTimeString();
        let logHtml = `[${timestamp}] << API 請求失敗 >>\n\n`;
        logHtml += `錯誤訊息: ${message}`;

        consoleOutput.innerHTML = `<span class="console-err">${logHtml}</span>`;
    }
});
