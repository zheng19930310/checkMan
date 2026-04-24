import torch
import torch.nn as nn
import torchvision.models as models

class GenderAgeNet(nn.Module):
    """性别年龄识别网络"""
    
    def __init__(self, num_genders=2):
        super(GenderAgeNet, self).__init__()
        
        # 使用预训练的ResNet18作为骨干网络
        backbone = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        
        # 移除最后的全连接层
        self.features = nn.Sequential(*list(backbone.children())[:-1])
        
        # 获取ResNet最后一层的输出维度
        num_features = backbone.fc.in_features
        
        # 性别分类头
        self.gender_head = nn.Sequential(
            nn.Linear(num_features, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_genders)
        )
        
        # 年龄回归头
        self.age_head = nn.Sequential(
            nn.Linear(num_features, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 1)
        )
    
    def forward(self, x):
        """前向传播"""
        features = self.features(x)
        features = features.view(features.size(0), -1)
        
        gender_output = self.gender_head(features)
        age_output = self.age_head(features)
        
        return gender_output, age_output

def create_model():
    """创建模型实例"""
    model = GenderAgeNet()
    return model
