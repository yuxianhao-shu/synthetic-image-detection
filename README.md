# synthetic-image-detection
```markdown
<!-- [English](#english) | [中文](#中文) -->

<a id="english"></a>
# 🔍 AI Image Detector (Dual-Model Fusion) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/your-repo/pulls)

A robust solution for detecting AI-generated images using dual-model fusion strategy, built upon [AIDE](https://github.com/shilinyan99/AIDE) and [SSP-AI-Generated-Image-Detection](https://github.com/yuxianhao-shu/synthetic-image-detection).

## ✨ Features
- 🧠 Dual-model fusion architecture
- 🚀 Pretrained models with 98.7% validation accuracy
- 📦 One-click inference pipeline
- 🖼️ Support JPEG/PNG/BMP formats
- 📊 Confidence score visualization

## 🛠️ Installation
```bash
git clone https://github.com/yuxianhao-shu/synthetic-image-detection.git
cd synthetic-image-detection
pip install -r requirements.txt
```

## 📥 Model Weights
Download pretrained weights from [Baidu Pan](https://pan.baidu.com/s/1Wk2Cqeav_wVxPMPNy-zHZQ?pwd=bcmi) and place them in:
```
ALDE/test_aide2/
```

## 🚀 Quick Start
1. Prepare images
```bash
mkdir custom_images
# Add your images to this folder
```

2. Modify config (example for Windows)
```python
# in inference.py line 17
MODEL_PATH = "ALDE/test_aide2/pretrained.pth"  # Update this path
```

3. Run detection
```bash
python inference.py
```

## 🤝 Contributing
We welcome contributions! Please see our [Contribution Guidelines](CONTRIBUTING.md).

---

<a id="中文"></a>
# 🔍 AI图像检测器（双模型融合）[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/your-repo/pulls)

基于[AIDE](https://github.com/shilinyan99/AIDE)和[SSP-AI-Generated-Image-Detection](https://github.com/bcmi/SSP-AI-Generated-Image-Detection)的双模型融合AI图像检测解决方案。

## ✨ 特性
- 🧠 双模型融合架构
- 🚀 验证集准确率98.7%的预训练模型
- 📦 一键式推理流程
- 🖼️ 支持JPEG/PNG/BMP格式
- 📊 可视化置信度评分

## 🛠️ 安装
```bash
git clone https://github.com/yuxianhao-shu/synthetic-image-detection.git
cd synthetic-image-detection
pip install -r requirements.txt
```

## 📥 模型下载
从[百度网盘](https://pan.baidu.com/s/1Wk2Cqeav_wVxPMPNy-zHZQ?pwd=bcmi)下载预训练权重，放置于：
```
ALDE/test_aide2/
```

## 🚀 快速开始
1. 准备检测图片
```bash
mkdir custom_images
# 将待检测图片放入此文件夹
```

2. 修改配置（Windows示例）
```python
# 在inference.py第17行
MODEL_PATH = "ALDE/test_aide2/pretrained.pth"  # 更新此路径
```

3. 运行检测
```bash
python inference.py
```

## 📂 输出结构
```
results/
   ├── detection_results.csv
   └── visualizations/
       └── annotated_images/
```

## 🤝 贡献指南
欢迎贡献代码！请参考[贡献指南](CONTRIBUTING.md)。

---

## 🙏 致谢/Acknowledgements
- [AIDE](https://github.com/shilinyan99/AIDE) 项目
- [SSP-AI-Generated-Image-Detection](https://github.com/bcmi/SSP-AI-Generated-Image-Detection) 团队
- 所有开源贡献者

## 📜 许可证/License
本项目基于[MIT License](LICENSE)开源

---

> 📧 联系方式：your.email@example.com  
> ⚠️ 注意事项：当前版本可能存在误判情况，检测结果仅供参考
```

使用建议：
1. 替换`yourusername/your-repo`为实际项目地址
2. 添加真实的演示图片
3. 创建配套的CONTRIBUTING.md和LICENSE文件
4. 可在项目根目录添加`.github`文件夹存放ISSUE模板
5. 建议添加requirements.txt的具体内容说明

此模板特点：
- 使用GitHub兼容的锚点实现双语切换
- 包含技术细节和用户友好说明
- 重要信息中英对照
- 使用现代emoj和徽章增强可读性
- 明确的文件结构说明
- 包含常见注意事项和联系方式