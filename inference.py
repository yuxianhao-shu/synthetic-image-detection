from AIDE.test_aide import run_aide_detection
from SSP.test_ssp import test_ssp

def multi_model_analysis():
    # 配置路径
    image_folder = "F:/synthetic-image-detection/custom_images"
    
    # 执行双模型检测
    aide_results = run_aide_detection(image_folder)
    ssp_results = test_ssp(image_folder=image_folder)
    
    # 创建结果映射表
    result_map = {}
    
    # 构建AIDE结果映射
    for item in aide_results:
        filename = item["filename"]
        result_map[filename] = {
            "AIDE_real": item["probability_real"],
            "AIDE_label": item["predicted_label"] == "真实图像"
        }
    
    # 合并SSP结果
    for item in ssp_results:
        filename = item["filename"]
        result_map[filename].update({
            "SSP_real": 1 - item["probability"],  # 转换真实概率
            "SSP_label": item["predicted_label"] == "真实图像"
        })
    
    # 计算最终结果
    final_output = []
    for filename, data in result_map.items():
        # 获取双模型状态
        aide_is_real = data["AIDE_label"]
        ssp_is_real = data["SSP_label"]
        
        # 决策逻辑
        if aide_is_real and ssp_is_real:
            # 双真实：取平均
            avg = (data["AIDE_real"] + data["SSP_real"]) / 2
            label = "真实图像"
        elif aide_is_real or ssp_is_real:
            # 单真实：取真实方的概率
            avg = data["AIDE_real"] if aide_is_real else data["SSP_real"]
            label = "真实图像"
        else:
            # 双AI：取AI概率平均
            avg = ((1 - data["AIDE_real"]) + (1 - data["SSP_real"])) / 2
            label = "AI生成"
        
        final_output.append({
            "filename": filename,
            "final_label": label,
            "combined_prob": avg
        })
    
    # 简洁输出
    print("\n综合检测报告：")
    for result in final_output:
        print(f"{result['filename']:20} => {result['final_label']} ({result['combined_prob']:.2%})")
    
    return final_output

if __name__ == "__main__":
    multi_model_analysis()