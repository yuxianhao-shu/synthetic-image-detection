import torch
from torch import nn
from SSP.networks.resnet import resnet50
from SSP.networks.srm_conv import SRMConv2d_simple
import torch.nn.functional as F
#输入图像 → 插值到256x256 → SRM特征提取 → ResNet50特征提取 → 二分类输出

class ssp(nn.Module):
    def __init__(self, pretrain=True):
        super().__init__()
        self.srm = SRMConv2d_simple()# SRM预处理层
        #print("SRM输出通道:", self.srm.out_channels) #SRM输出通道数
        self.disc = resnet50(pretrained=True) #ResNet主干网络
        #print("ResNet输入通道:", self.disc.conv1.in_channels)  # 必须为30
        self.disc.fc = nn.Linear(2048, 1)# 最后一层为二分类

    def forward(self, x):
        x = F.interpolate(x, (256, 256), mode='bilinear')#统一输入尺寸
        x = self.srm(x) #应用SRM滤波器
        x = self.disc(x) #通过ResNet50
        #x=self.disc.fc(x)
        return x


if __name__ == '__main__':
    model = ssp(pretrain=True)
    print(model)
