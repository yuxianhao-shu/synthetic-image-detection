# synthetic-image-detection
<a id="中文"></a>
# 🔍 AI图像检测器（双模型融合）[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/your-repo/pulls)

基于[AIDE](https://github.com/shilinyan99/AIDE)和[SSP-AI-Generated-Image-Detection](https://github.com/bcmi/SSP-AI-Generated-Image-Detection)的双模型融合AI图像检测解决方案。

## ✨ 特性
- 🧠 双模型融合架构
- 🚀 验证集准确率98.7%的预训练模型
- 📦 一键式推理流程
- 🖼️ 支持JPEG/PNG/JPG格式
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
synthetic-image-detection\AIDE
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
f3.jpg               => 真实图像 (52.49%)
ff1.jpg              => AI生成 (90.20%)
ff2.png              => 真实图像 (86.30%)
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

> 📧 联系方式：yuxianhao23@gmail.com 
> ⚠️ 注意事项：当前版本可能存在误判情况，检测结果仅供参考
```