import os
import json
from typing import Optional, Dict, Any
from .models import BicModelConfig, ModelProvider

class BicRouter:
    """
    BIC Router: 实现数据驱动的模型路由。
    支持 “Thinking Budget” (推理预算) 控制。
    """
    
    def __init__(self, config_path: str):
        self.models = self._load_config(config_path)

    def _load_config(self, path: str) -> Dict[str, BicModelConfig]:
        with open(path, 'r') as f:
            data = json.load(f)
        return {m["model_name"]: BicModelConfig(**m) for m in data}

    def get_generation_params(self, model_name: str) -> Dict[str, Any]:
        """
        获取模型的推断参数，包含 “Thinking Budget”。
        """
        model_cfg = self.models.get(model_name)
        if not model_cfg:
            return {"max_tokens": 1024}
        
        params = {
            "model": model_cfg.model_name,
            "max_tokens": 4096
        }
        
        # 1. 实现 Thinking Budget 逻辑
        if model_cfg.thinking_enabled:
            # 针对 Anthropic / OpenRouter 的标准参数
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": model_cfg.thinking_budget
            }
            # 推理模型通常需要更高的总 Token 限制
            params["max_tokens"] = max(params["max_tokens"], model_cfg.thinking_budget + 1024)
            
        # 2. 注入“分片蒸馏”与“元数据对齐”逻辑 (生蛋理论核心)
        if model_cfg.distilled_history:
            # 递归式压缩的历史摘要 (Recursive History Compression)
            params["system_prompt_appendix"] = f"\n\n[Recursive History Compression]:\n{model_cfg.distilled_history}"
            
        if model_cfg.hard_constraints:
            # 标准化元数据带来的“零成本对齐” (Zero-Shot Alignment)
            constraints_str = json.dumps(model_cfg.hard_constraints, indent=2, ensure_ascii=False)
            params["system_prompt_appendix"] = params.get("system_prompt_appendix", "") + f"\n\n[Zero-Shot Alignment - Hard Constraints]:\n{constraints_str}"

        return params

    def route(self, task_complexity: str) -> str:
        """
        根据任务复杂度选择比克形态。
        """
        if task_complexity == "HIGH":
            # 返回具备 Thinking 能力的模型
            for m in self.models.values():
                if m.thinking_enabled:
                    return m.model_name
        return list(self.models.keys())[0]  # 默认回退
