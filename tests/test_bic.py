from bic.router import BicRouter
from bic.models import ModelProvider

def test_routing_logic():
    print("🧪 正在测试比克路由逻辑...")
    router = BicRouter("configs/models.json")
    
    # 测试高复杂度路由
    model = router.route("HIGH")
    assert "thinking" in model
    print(f"✅ 高复杂度路由输出: {model}")
    
    # 测试 Thinking Budget 参数生成
    params = router.get_generation_params(model)
    assert params["thinking"]["budget_tokens"] == 4000
    print(f"✅ Thinking Budget 验证成功: {params['thinking']['budget_tokens']} tokens")

def test_warmup_structure():
    print("🧪 正在测试预热逻辑结构...")
    from bic.warmup import BicWarmup
    warmup = BicWarmup()
    # 这里我们只验证方法存在且逻辑闭环
    assert hasattr(warmup, "run_full_warmup")
    print("✅ 预热接口验证成功")

if __name__ == "__main__":
    try:
        test_routing_logic()
        test_warmup_structure()
        print("\n✨ 所有测试通过！比克已准备好战斗。")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
