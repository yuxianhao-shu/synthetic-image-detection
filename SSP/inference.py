import cv2
import torch
from SSP.networks.ssp import ssp
from torchvision import transforms
from SSP.utils.patch import patch_img
from PIL import Image
import os
import numpy as np

#加载模型
model = ssp().cpu()  # 使用CPU模式
model.load_state_dict(
    torch.load('pretrained/midjourney.pth', map_location='cpu')
)
model.eval()

#预处理流程保持不变
patch_func = transforms.Lambda(lambda img: patch_img(img, 32, 256))
trans = transforms.Compose([
    patch_func,
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

# 图像处理
image_folder = "custom_images"
if os.path.exists(image_folder):
    print("\n批量检测结果：")
    
    # 添加文件过滤
    allowed_ext = ['.jpg', '.jpeg', '.png']
    
    for filename in sorted(os.listdir(image_folder)):
        # 构建完整路径
        img_path = os.path.join(image_folder, filename)
        
        # 跳过非图像文件
        if not os.path.isfile(img_path):
            continue
        if not filename.lower().endswith(tuple(allowed_ext)):
            print(f"跳过非图像文件: {filename}")
            continue
        
        try:
            # 图像处理
            with Image.open(img_path) as img:
                img = img.convert('RGB')
                input_tensor = trans(img).unsqueeze(0)
                
                # 预测
                with torch.no_grad():
                    out = model(input_tensor)
                    prob = torch.sigmoid(out).item()
                
                # 输出结果
                print(f"{filename:20s} => {'AI生成' if prob > 0.5 else '真实图像'} ({prob:.2%})")
                
        except Exception as e:
            print(f"处理文件 {filename} 失败: {str(e)}")