import os
from pathlib import Path
import argparse
from uvprojxproject import UVPROJXProject

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
        print(extensions);
    
    return matched_files


if __name__ == '__main__':
    current_dir = os.getcwd()
    current_file = os.path.basename(__file__)
    parent_dir = Path(__file__).parent.parent.absolute()
    matched_files = get_files_by_extensions(parent_dir, ['uvprojx'])
    print(matched_files)
    for file in matched_files:
        file_path = str(file.parent)
        file_name = file.name
        parser = argparse.ArgumentParser(description='This is a demo script', add_help=True)
        parser.add_argument('--parent_dir', nargs='?', default=file_path,help="Root directory of project")
        args = parser.parse_args()
        print(args)
	    #"--ewp", help="Search for *.EWP file in project structure", action='store_true')
        #parser.add_argument("--uvprojx", help="Search for *.UPROJX file in project structure", action='store_true')
        project= UVPROJXProject(args, file)
        project.parseProject()
        #print(project)

