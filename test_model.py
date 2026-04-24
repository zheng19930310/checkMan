import torch
from model import create_model

def test_model():
    """测试模型是否可以正常创建和运行"""
    print("测试模型创建...")
    model = create_model()
    
    # 创建一个假的输入张量 (batch_size=1, channels=3, height=224, width=224)
    dummy_input = torch.randn(1, 3, 224, 224)
    
    print("测试前向传播...")
    with torch.no_grad():
        gender_output, age_output = model(dummy_input)
    
    print(f"性别输出形状: {gender_output.shape}")
    print(f"年龄输出形状: {age_output.shape}")
    
    print("模型测试通过！")

if __name__ == "__main__":
    test_model()
