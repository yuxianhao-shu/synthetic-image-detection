import os
import time
import stat

class FolderCleaner:
    """安全删除文件夹内所有文件（保留目录结构）"""
    def __init__(self, folder_path, delete_timeout=3):
        self.folder_path = folder_path
        self.delete_timeout = delete_timeout

    def _unlock_file(self, path):
        """解除文件锁定（Windows只读属性处理）"""
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWRITE)

    def _safe_delete_file(self, file_path):
        """带重试机制的文件删除"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if os.name == 'nt':  # Windows系统需要处理只读文件
                    self._unlock_file(file_path)
                os.remove(file_path)
                print(f"✅ 已删除：{file_path}")
                return True
            except PermissionError:
                print(f"⏳ 文件被占用，等待重试 ({attempt+1}/{max_retries})")
                time.sleep(self.delete_timeout)
            except Exception as e:
                print(f"❌ 删除失败 [{file_path}]: {str(e)}")
                return False
        return False

    def clean(self):
        """执行清理（保留所有文件夹）"""
        if not os.path.exists(self.folder_path):
            print(f"⚠️ 路径不存在: {self.folder_path}")
            return

        # 递归遍历所有子目录
        for root, _, files in os.walk(self.folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):
                    self._safe_delete_file(file_path)

        print(f"🗃️ 已完成清理，文件夹结构保留在: {self.folder_path}")

if __name__ == "__main__":
    cleaner = FolderCleaner(
        folder_path = "videos",  # 要清理的目标文件夹
        delete_timeout = 2       # 重试等待时间（秒）
    )
    cleaner.clean()