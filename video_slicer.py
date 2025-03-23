import cv2
import os
import random
import time
import ctypes
import shutil

class VideoFrameExtractor:
    def __init__(self, video_path, output_folder, delete_source=False, video_basename=''):
        """
        初始化视频帧提取器
        
        :param video_path: 输入视频文件路径
        :param output_folder: 输出文件夹路径
        :param delete_source: 是否删除处理后的源视频文件（默认False）
        :param video_basename: 视频文件基名（用于生成唯一文件名）
        """
        self.video_path = video_path
        self.output_folder = output_folder
        self.delete_source = delete_source 
        self.cap = None
        self.current_second = -1
        self.reservoir_frame = None
        self.reservoir_count = 0
        self.frame_number = 0
        self.video_basename = video_basename 
        self.lock_file = None

    def _initialize_video(self):
        """初始化视频捕获对象"""
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise ValueError("无法打开视频文件")
        return self.cap.get(cv2.CAP_PROP_FPS)

    def _prepare_output(self):
        """创建输出目录"""
        os.makedirs(self.output_folder, exist_ok=True)

    def _process_second(self, second):
        """处理每秒钟的帧保存"""
        if self.reservoir_count > 0:
            # 新增视频基名到文件名
            output_path = os.path.join(
                self.output_folder, 
                f"{self.video_basename}_sec_{second:04d}.jpg"
            )
            cv2.imwrite(output_path, self.reservoir_frame)
            print(f"保存：{self.video_basename} 第 {second} 秒的帧")

        # 重置蓄水池状态
        self.current_second = second
        self.reservoir_count = 0
        self.reservoir_frame = None

    def _reservoir_sampling(self, frame):
        """蓄水池抽样算法实现"""
        self.reservoir_count += 1
        if self.reservoir_count == 1:
            self.reservoir_frame = frame.copy()
        else:
            if random.randrange(self.reservoir_count) == 0:
                self.reservoir_frame = frame.copy()

    def process(self):
        """
        执行视频处理流程
        """
        # 初始化环境
        self._prepare_output()
        fps = self._initialize_video()
        
        try:
            self.lock_file = open(os.path.join(self.output_folder, "__lock__"), "w")
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break  # 视频结束

                # 计算当前时间（秒）
                timestamp_ms = self.cap.get(cv2.CAP_PROP_POS_MSEC)
                timestamp = timestamp_ms / 1000 if timestamp_ms > 0 else self.frame_number / fps
                current_second = int(timestamp)

                # 检测新秒数
                if current_second != self.current_second:
                    if self.current_second != -1:
                        self._process_second(self.current_second)
                    self.current_second = current_second

                # 执行抽样算法
                self._reservoir_sampling(frame)
                self.frame_number += 1

            # 处理最后一秒
            if self.reservoir_count > 0:
                self._process_second(self.current_second)

        finally:
            if self.cap:
                self.cap.release()
            if self.lock_file:
                self.lock_file.close()

        print("视频处理完成")

    def _safe_cleanup_source_video(self):
        """安全清理源视频文件（改进版）"""
        max_retries = 1
        retry_delay = 0.1  # 秒
        
        for attempt in range(max_retries):
            if not os.path.isfile(self.video_path):
                print(f"[{self.video_path}] 文件已自动删除")
                return
                
            try:
                os.remove(self.video_path)
                print(f"[{self.video_path}] 删除成功")
                return
            except PermissionError as e:
                if attempt < max_retries - 1:
                    print(f"[{self.video_path}] 删除被阻止（尝试 {attempt+1}/{max_retries}），等待后重试...")
                    time.sleep(retry_delay)
                else:
                    print(f"[{self.video_path}] 删除失败：\n错误码 {e.winerror}\n原因：文件可能被其他程序占用或权限不足")
                    print("建议：\n1. 确保没有程序正在使用该文件\n2. 手动删除文件\n3. 检查文件权限")
            except Exception as e:
                print(f"[{self.video_path}] 删除失败：{str(e)}")
                break

class VideoFolderProcessor:
    """视频文件夹处理器（改进版）"""
    def __init__(self, input_folder, output_base, delete_sources=True):
        """
        初始化视频文件夹处理器
        
        :param input_folder: 输入视频文件夹路径
        :param output_base: 统一的输出文件夹路径
        :param delete_sources: 是否删除处理后的源视频（默认True）
        """
        self.input_folder = input_folder
        self.output_base = output_base
        self.delete_sources = delete_sources
        self.video_extensions = {'.mp4', '.avi', '.mov', '.mkv'}  # 支持的视频格式

    def process_folder(self):
        """处理整个视频文件夹"""
        print(f"\n开始处理文件夹: {self.input_folder}")
        
        # 确保输出目录存在
        os.makedirs(self.output_base, exist_ok=True)
        print(f"输出目录已创建: {self.output_base}")

        # 遍历文件夹中的所有文件
        for filename in os.listdir(self.input_folder):
            file_path = os.path.join(self.input_folder, filename)
            
            # 只处理视频文件
            if os.path.isfile(file_path) and os.path.splitext(filename)[1] in self.video_extensions:
                print(f"\n处理文件: {filename}")
                
                # 提取视频基名（去除扩展名）
                video_basename = os.path.splitext(filename)[0]
                
                # 初始化帧提取器（传入视频基名）
                extractor = VideoFrameExtractor(
                    video_path=file_path,
                    output_folder=self.output_base,
                    delete_source=self.delete_sources,
                    video_basename=video_basename
                )
                
                # 执行处理
                extractor.process()
                
        print("\n处理完成")

if __name__ == "__main__":
    # 使用示例
    processor = VideoFolderProcessor(
        input_folder="videos",   # 输入视频文件夹路径
        output_base="custom_images", # 统一输出文件夹路径
        delete_sources=True          # 处理完成后删除源视频
    )
    
    processor.process_folder()