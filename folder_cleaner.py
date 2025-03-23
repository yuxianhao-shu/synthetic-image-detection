import os
import shutil
import time

class FolderCleaner:
    """专门用于清理文件夹的类"""
    def __init__(self, folder_path, delete_timeout=5):
        """
        :param folder_path: 要清理的文件夹路径
        :param delete_timeout: 删除操作等待时间（秒）
        """
        self.folder_path = folder_path
        self.delete_timeout = delete_timeout

    def _safe_delete_file(self, filepath):
        """安全删除单个文件"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                os.remove(filepath)
                #print(f"✅ 删除成功：{filepath}")
                return
            except PermissionError:
                #print(f"⏳ 文件被占用，等待 {self.delete_timeout} 秒后重试...")
                time.sleep(self.delete_timeout)
            except Exception as e:
                #print(f"❌ 删除失败：{filepath} - {str(e)}")
                break

    def clean(self):
        """执行文件夹清理"""
        #print(f"\n开始清理文件夹：{self.folder_path}")
        if os.path.isdir(self.folder_path):
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                if os.path.isfile(file_path):
                    self._safe_delete_file(file_path)
            shutil.rmtree(self.folder_path, ignore_errors=True)
            #print(f"✅ 清理完成：{self.folder_path}")
        else:
            print(f"⚠️ 目标路径不是文件夹")

if __name__ == "__main__":
    cleaner = FolderCleaner(
        folder_path="videos",  # 要删除的文件夹路径
        delete_timeout=1      # 设置删除等待时间
    )
    cleaner.clean()
    print("文件夹清理完成")