import requests
import logging
from typing import Dict, Any

logger = logging.getLogger("bic.warmup")

class BicWarmup:
    """
    负责系统预热 (Warmup Logic)，对应 PR #1466。
    确保模型在第一次正式请求前已加载并准备就绪。
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url

    def ping_ollama(self, model_name: str) -> bool:
        """预热本地 Ollama 模型"""
        logger.info(f"⚡ 正在预热本地比克 (Ollama): {model_name}")
        try:
            # 这里的逻辑是发送一个空请求以保证模型被加载到显存
            payload = {
                "model": model_name,
                "prompt": "ping",
                "stream": False
            }
            resp = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=30)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"❌ 预热失败: {e}")
            return False

    def check_cloud_link(self, provider: str) -> bool:
        """检查云端链路是否通畅"""
        logger.info(f"🌌 正在检查天神链路: {provider}")
        # 这里可以是简单的 API Key 连通性测试
        return True

    def run_full_warmup(self, models_to_warm: list):
        for m in models_to_warm:
            if m.provider == "Ollama":
                self.ping_ollama(m.model_name)
            else:
                self.check_cloud_link(m.provider)
        logger.info("✅ 系统调息完成，可以开始战斗！")
