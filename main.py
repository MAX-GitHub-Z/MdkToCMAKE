import os
from pathlib import Path
import argparse
from uvprojxproject import UVPROJXProject
import cmake
import shutil

"""
Class to parse UVPROJX project file formatfrom
//查找当前目录下的对应的uvprojx文件class UVPROJXProject:
"""
def get_files_by_extensions(directory, extensions):
    """
    获取匹配任意一个后缀的文件
    
    :param directory: 要搜索的目录路径
    :param extensions: 后缀元组如 ('.jpg', '.png')
    :return: 匹配的文件列表
    """
    folder = Path(directory)
    
    # 确保扩展名不以点开头（pathlib会自动处理）
    extensions = [ext.lstrip('.') for ext in extensions]
    
    matched_files = []
    
    for ext in extensions:
        matched_files.extend(folder.rglob(f'*.{ext}'))
        #print(extensions);
    
    return matched_files

def copy_file_with_custom_name(source_file, target_file):
    """
    跨平台复制文件到指定路径（可自定义文件名）
    不存在则创建目录，存在则覆盖文件
    
    Args:
        source_file: 源文件路径
        target_file: 目标文件路径（可包含自定义文件名）
    """
    try:
        # 转换为 Path 对象（自动处理不同操作系统的路径分隔符）
        source = Path(source_file)
        target = Path(target_file)
        
        # 检查源文件是否存在
        if not source.exists():
            raise FileNotFoundError(f"源文件不存在: {source}")

        
        # 确保目标目录存在
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制文件（自动覆盖已存在的文件）
        shutil.copy2(source, target)
        
        print(f"✅ 文件复制成功: {source} -> {target}")
        return True
        
    except Exception as e:
        print(f"❌ 文件复制失败: {e}")
        return False
    
def are_paths_identical(path1, path2):
    """
    判断两个文件路径是否完全相同（包括文件名和后缀）
    
    Args:
        path1: 第一个文件路径
        path2: 第二个文件路径
    
    Returns:
        bool: 如果路径指向同一个文件返回True，否则返回False
    """
    try:
        # 转换为Path对象并解析绝对路径
        p1 = Path(path1).resolve()
        p2 = Path(path2).resolve()
        
        # 比较绝对路径
        #print("对比结果：",p1,p2,p1 == p2)
        return p1 == p2
    except Exception as e:
        print(f"路径比较错误: {e}")
        return False

if __name__ == '__main__':
    current_dir = os.getcwd()
    current_file = os.path.basename(__file__)
    parent_dir = Path(__file__).parent.parent.absolute()
    matched_files = get_files_by_extensions(parent_dir, ['uvprojx'])
    #print(matched_files)
    """设置CMAKE放置的位置 默认位置为 项目父目录下新建 cmake文件夹中
    """
    cmake_Pro_file = parent_dir
    """循环处理 并提取不同项目的 信息
    """

    for file in matched_files:
        file_path = str(file.parent)
        file_name = file.name
        parser = argparse.ArgumentParser(description='This is a demo script', add_help=True)
        parser.add_argument('--parent_dir', nargs='?', default=file_path,help="Root directory of project")
        args = parser.parse_args()
        #print(args)
	    #"--ewp", help="Search for *.EWP file in project structure", action='store_true')
        #parser.add_argument("--uvprojx", help="Search for *.UPROJX file in project structure", action='store_true')
        project= UVPROJXProject(args, file)
        project.parseProject()
        CmakeFile = cmake.CMake(project.getProject(), cmake_Pro_file)
        CmakeFile.AnalyseCmake()
        CmakeFile.populateCMake()
    cmake_path = parent_dir/"cmake"
    cmake_path = Path(cmake_path)
    cmake_rule_path =  Path(cmake_path/'Rule.cmake')
    if cmake_rule_path.exists():
        os.remove(cmake_rule_path)

    cmake_dir = get_files_by_extensions(cmake_path, ['.cmake'])
    cmake_lenth = len(cmake_dir)
    print(cmake_dir,cmake_lenth)
    for cmake_file in cmake_dir:
        if cmake_lenth == 1:
            print("该项目只有一个工程 自动复制该编译配置 并进行编译")
            print(cmake_rule_path)
            copy_file_with_custom_name(cmake_file, cmake_rule_path)
            projectName = Path(cmake_file).stem
            

    CmakeFile.CmakeCopyList(projectName)

    


