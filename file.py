import os
import shutil
from myexception import dstPathException


class File:

    @staticmethod
    def move_to(src: str, dst: str) -> bool:
        shutil.move(src, dst)

    @staticmethod
    def get_list(src: str,
                 size_limit: tuple[int, int] = (0, -1),
                 ext_limit: list[str] = [],
                 iteration=False) -> list[str]:
        if not os.path.exists(src):
            return []
        elif not iteration:
            file_paths = []
            for filename in os.listdir(src):  # 遍历文件夹
                filepath = os.path.join(src, filename)
                if os.path.isfile(filepath):
                    if not File.check_file(filepath,
                                           size_limit=size_limit,
                                           ext_limit=ext_limit):
                        continue
                    else:
                        file_paths.append(filepath)
            print(file_paths)
            return file_paths
        else:
            file_paths = []
            for root, directories, files in os.walk(src):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    if not File.check_file(filepath,
                                           size_limit=size_limit,
                                           ext_limit=ext_limit):
                        continue
                    else:
                        file_paths.append(filepath)
            return file_paths

    @staticmethod
    def check_file(path, size_limit: tuple[int, int],
                   ext_limit: list[str]) -> bool:
        if size_limit[0] > 0 or size_limit[1] != -1:  # 如果限制文件大小
            file_size = os.path.getsize(path) / float(1024)
            if size_limit[1] != -1:
                if not size_limit[0] < file_size < size_limit[1]:  # 不符合大小限制
                    return False
            else:
                if not size_limit[0] < file_size:  # 不符合大小限制
                    return False
        if len(ext_limit):  # 如果限制文件扩展
            if os.path.splitext(path)[-1][1:] not in ext_limit:
                return False
        return True

    @staticmethod
    def list_move_to(src: list[str], dst: str) -> bool:
        if not os.path.isdir(dst):
            raise dstPathException
        try:
            for file_path in src:
                (_, file_name) = os.path.split(file_path)
                dst_file_path = os.path.join(dst, file_name)
                shutil.move(file_path, dst_file_path)
            return True
        except:
            raise dstPathException
