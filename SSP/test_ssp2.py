import cv2
import torch
from SSP.networks.ssp import ssp
from torchvision import transforms
from SSP.utils.patch import patch_img
from PIL import Image
import os
import numpy as np

def detect_images(
    image_folder: str,
    model_path: str = 'pretrained/midjourney.pth',
    device: str = 'cpu',
    threshold: float = 0.5
) -> list:  # 修改返回类型为列表
    """
    返回格式:
    [
        {
            "filename": "image1.jpg",
            "model": "SSP",
            "predicted_label": "AI生成",
            "probability": 0.85
        },
        ...
    ]
    """
    model = ssp().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    patch_func = transforms.Lambda(lambda img: patch_img(img, 32, 256))
    trans = transforms.Compose([
        patch_func,
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    results = []  # 改为列表存储
    allowed_ext = ('.jpg', '.jpeg', '.png')

    for filename in sorted(os.listdir(image_folder)):
        img_path = os.path.join(image_folder, filename)
        
        if not (os.path.isfile(img_path) and filename.lower().endswith(allowed_ext)):
            continue
        
        try:
            with Image.open(img_path) as img:
                input_tensor = trans(img.convert('RGB')).unsqueeze(0).to(device)
                
                with torch.no_grad():
                    out = model(input_tensor)
                    prob = torch.sigmoid(out).item()
                
                results.append({
                    "filename": filename,
                    "model": "SSP",
                    "predicted_label": "AI生成" if prob > threshold else "真实图像",
                    "probability": prob
                })
                
        except Exception as e:
            print(f"[ERROR] 处理失败 {filename}: {str(e)}")
    
    return results

def test_ssp(
    image_folder: str = "custom_images",
    model_path: str = None,
    device: str = "cpu"
) -> list:
    if model_path is None:
        model_path = os.path.join(
            os.path.dirname(__file__),
            "pretrained/midjourney.pth"
        )
    
    return detect_images(  # 直接返回结果列表
        image_folder=image_folder,
        model_path=model_path,
        device=device
    )

if __name__ == "__main__":
    results = test_ssp()
    for item in results:
        print(f"{item['filename']:20s} => {item['predicted_label']} ({item['probability']:.4f})")