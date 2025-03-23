import torch
from PIL import Image
from torchvision import transforms
import AIDE.models.AIDE as AIDE
import argparse
import os
from AIDE.data.dct import DCT_base_Rec_Module

IMAGE_FOLDER = "F:/synthetic-image-detection/custom_images"
RESUME_PATH = "F:/synthetic-image-detection/AIDE/sd14_train.pth"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model():
    device = torch.device(DEVICE)
    model = AIDE.__dict__["AIDE"](resnet_path=None, convnext_path=None)  
    model.to(device)
    if os.path.exists(RESUME_PATH):
        checkpoint = torch.load(RESUME_PATH, map_location=device)
        model.load_state_dict(checkpoint['model'], strict=False)
    model.eval()
    return model

def preprocess_image(image_path, input_size=224):
    transform_before_test = transforms.Compose([transforms.ToTensor()])
    transform_train = transforms.Compose([
        transforms.Resize([256, 256], antialias=True),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    dct = DCT_base_Rec_Module()
    image = Image.open(image_path).convert('RGB')
    image = transform_before_test(image)
    x_minmin, x_maxmax, x_minmin1, x_maxmax1 = dct(image)
    x_0 = transform_train(image)
    x_minmin = transform_train(x_minmin)
    x_maxmax = transform_train(x_maxmax)
    x_minmin1 = transform_train(x_minmin1)
    x_maxmax1 = transform_train(x_maxmax1)
    return torch.stack([x_minmin, x_maxmax, x_minmin1, x_maxmax1, x_0], dim=0)

def inference(model, image, device):
    image = image.to(device)
    with torch.no_grad():
        outputs = model(image)
    probabilities = torch.softmax(outputs, dim=1)
    _, predicted = torch.max(outputs, 1)
    return predicted, probabilities

def main():
    model = load_model()
    device = torch.device(DEVICE)
    results = []  # 存储结果的列表

    if not os.path.isdir(IMAGE_FOLDER):
        print(f"Image folder {IMAGE_FOLDER} does not exist.")
        return results

    SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png')
    
    for filename in os.listdir(IMAGE_FOLDER):
        file_path = os.path.join(IMAGE_FOLDER, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(SUPPORTED_EXTENSIONS):
            try:
                image = preprocess_image(file_path).unsqueeze(0)
                predicted, probabilities = inference(model, image, device)
                
                # 提取概率值（假设二分类）
                prob_real = probabilities[0, 1].item()  # 真实图像的概率
                prob_ai = probabilities[0, 0].item()    # AI生成的概率
                
                # 将结果存入字典
                result = {
                    "filename": filename,
                    "predicted_label": "真实图像" if predicted.item() == 1 else "AI生成",
                    "probability_real": prob_real,
                    "probability_ai": prob_ai
                }
                results.append(result)
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    return results  # 返回结果数组

def run_aide_detection(image_folder=None):
    """对外暴露的检测接口"""
    global IMAGE_FOLDER
    if image_folder:
        IMAGE_FOLDER = image_folder  # 允许动态指定检测目录
    return main()

if __name__ == "__main__":
    # 保留独立运行能力
    result_data = run_aide_detection()
    for item in result_data:
        print(f"{item['filename']:20s} => {item['predicted_label']} (真实概率: {item['probability_real']:.4f}, AI概率: {item['probability_ai']:.4f})")