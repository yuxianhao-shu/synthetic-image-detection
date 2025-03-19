import cv2
import os
import random

class VideoFrameExtractor:
    def __init__(self, video_path, output_folder):
        """
        初始化视频帧提取器
        
        :param video_path: 输入视频文件路径
        :param output_folder: 输出文件夹路径
        """
        self.video_path = video_path
        self.output_folder = output_folder
        self.cap = None
        self.current_second = -1
        self.reservoir_frame = None
        self.reservoir_count = 0
        self.frame_number = 0

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
            output_path = os.path.join(
                self.output_folder, 
                f"sec_{second:04d}.jpg"
            )
            cv2.imwrite(output_path, self.reservoir_frame)
            print(f"保存：第 {second} 秒的帧")

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
            print("视频处理完成")

if __name__ == "__main__":
    # 直接在代码中指定路径
    extractor = VideoFrameExtractor(
        video_path="testvideo.mp4",  # 替换为你的视频路径
        output_folder="custom_images"  # 指定输出目录
    )
    
    extractor.process()