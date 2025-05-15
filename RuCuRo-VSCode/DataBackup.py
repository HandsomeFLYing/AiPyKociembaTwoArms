import datetime
import shutil
import os

def Backuo():
        print("?")
        # 示例：将 'source_folder' 复制到当前目录下以当前时间命名的文件夹
        source_folder = "data"  # 替换为实际的源文件夹路径
        picture = "picture"
        if not os.path.exists(source_folder):
            print(f"（备份）错误：源文件夹 '{source_folder}' 不存在")
        if not os.path.exists(picture):
            print(f"（备份）错误：源文件夹 '{picture}' 不存在")
        # 如果没有指定目标位置，使用当前时间创建文件夹
        if None is None:
            time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            data_time = "backup/" + time
            picture_time = "test/" + time
            parent_dir = os.getcwd()  # 当前工作目录
            target_dir_1 = os.path.join(parent_dir, data_time)
            target_dir_2 = os.path.join(parent_dir, picture_time)
        
        # 复制文件夹
        try:
            shutil.copytree(source_folder, target_dir_1)
            print(f"（备份）成功复制文件夹到: {target_dir_1}")
            
        except FileExistsError:
            print(f"（备份）错误：目标文件夹 '{target_dir_1}' 已存在")
        except Exception as e:
            print(f"（备份）错误：复制过程中出现问题: {e}")

        try:
            shutil.copytree(picture, target_dir_2)
            print(f"（备份）成功复制文件夹到: {target_dir_2}")
        except FileExistsError:
            print(f"（备份）错误：目标文件夹 '{target_dir_2}' 已存在")
        except Exception as e:
            print(f"（备份）错误：复制过程中出现问题: {e}")
