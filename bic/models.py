import json
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ModelProvider(str, Enum):
    OPENROUTER = "OpenRouter"
    GOOGLE = "Google"
    OLLAMA = "Ollama"

class BicModelConfig(BaseModel):
    display_name: str
    model_name: str
    provider: ModelProvider
    thinking_enabled: bool = False
    thinking_budget: Optional[int] = 2000  # Default 2000 tokens
    
    # 理论支撑字段
    distilled_history: Optional[str] = None  # 递归式压缩的历史摘要 (Recursive History Compression)
    hard_constraints: Optional[Dict[str, Any]] = None  # 标准化元数据约束 (Zero-Shot Alignment)

def load_config(path: str) -> List[BicModelConfig]:
    with open(path, 'r') as f:
        data = json.load(f)
    return [BicModelConfig(**d) for d in data]
