from inference import multi_model_analysis
from folder_cleaner import FolderCleaner
from video_slicer import VideoFolderProcessor,VideoFrameExtractor
if __name__ == "__main__":
    processor = VideoFolderProcessor(
        input_folder="videos",   # 输入视频文件夹路径
        output_base="custom_images", # 统一输出文件夹路径
        delete_sources=True          # 处理完成后删除源视频
    )
    processor.process_folder()
    multi_model_analysis()
    cleaner = FolderCleaner(
        folder_path="videos",  # 要删除的文件夹路径
        delete_timeout=1      # 设置删除等待时间
    )
    cleaner.clean()
    print("\n文件夹清理完成")