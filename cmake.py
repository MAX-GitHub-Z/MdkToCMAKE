# -*- coding: utf-8 -*-

import os
from pathlib import Path
import shutil

def safe_create_file_structure(base_dir, folder_name, file_name,file_cover = False, content="",indent=0):
    """
    安全创建文件夹和文件结构
    
    Args:
        base_dir (str): 基础目录
        folder_name (str): 文件夹名称
        file_name (str): 文件名称
        content (str): 文件内容
    
    Returns:
        bool: 是否成功创建了文件（不包括已存在的情况）
    """
    if True:
        # 转换为Path对象
        base_path = Path(base_dir)
        folder_path = base_path / folder_name
        file_path = folder_path / file_name
        
        print(f"目标路径: {file_path}")
        
        # 检查并创建文件夹
        if not folder_path.exists():
            print(f"创建文件夹: {folder_path}")
            folder_path.mkdir(parents=True, exist_ok=True)
        else:
            print(f"文件夹已存在: {folder_path}")
        
        # 检查文件是否存在
        if file_path.exists():
            if file_cover:
                print(f"文件已存在，进行覆盖操作: {file_path}")
            else:
                print(f"文件已存在，跳过创建 不覆盖: {file_path}")
                return False
            #return False
        

        # 创建文件
        print(f"创建文件: {file_path}")
        
        # 处理不同操作系统的换行符
        #if os.linesep != '\n':
        #    content = content.replace('\n', os.linesep)
        
        # 写入文件        
        file_path.write_text(content, encoding='utf-8')
        
        # 验证文件创建成功
        if file_path.exists() and file_path.is_file():
            file_size = file_path.stat().st_size
            print(f"✓ 文件创建成功，大小: {file_size} 字节")
            return True
        else:
            print("✗ 文件创建失败")
            return False
            
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
    

def process_relative_path(relative_path):
    """
    处理相对路径：去除开头的所有 "../"，并在最终输出时添加一个 "../"
    
    Args:
        relative_path (str): 输入相对路径
        
    Returns:
        str: 处理后的路径
    """
    # 将路径转换为 Path 对象
    path_obj = Path(relative_path)
    
    # 获取路径的所有部分
    parts = list(path_obj.parts)
    
    # 去除开头的所有 ".."
    while parts and parts[0] == "..":
        parts.pop(0)
    
    # 重新构建路径
    if parts:
        processed_path = Path(*parts)
    else:
        processed_path = Path(".")
    
    # 在开头添加一个 "../"
    final_path = Path("..") / processed_path
    
    return str(final_path)




class CMake (object):
    
    def __init__(self, project, path):
        
        self.path = path
        self.project = project
        self.context = {}
        self.Cmake = {}
        #print(self.path)
    
    def AnalyseCmake(self):
        """
        AnalyseCmake 的 Docstring
        
        :param self: 解析生成对应工程的.CMAKE文件 或生成对应的.CMAKE文件 
        """
        cmake_file = self.path
        cmake_file_name = self.project['name'].text + ".cmake"
        safe_create_file_structure(cmake_file, "cmake", cmake_file_name)
        #此处应该读取 手动配置的 CMAKE编译选项
        self.Cmake['CMAKE_C_FLAGS_MANUAL']= ''
        self.Cmake['CMAKE_LINKER_FILE'] = ''

    def populateCMake (self):
        """ Generate CMakeList.txt file for building the project
        """

        # For debug run cmake -DCMAKE_BUILD_TYPE=Debug or Release
        cmake = {}
        #fpu = '-mfpu=fpv5-sp-d16 -mfloat-abi=softfp'
        fpu = ''
        core =  self.project['AdsCpuType'].strip('"\'')
        core = '-mcpu='+core.lower()
        print("当前生成项目使用的 处理器内核为："+core)

        cmake['version'] = 'cmake_minimum_required(VERSION 3.12)'
        cmake['language'] =  '# Enable CMake support for ASM and C languages \n enable_language(C ASM)'
        cmake['project'] = '# Set the project name \n set(CMAKE_PROJECT_NAME '+self.project['name'] +')\n'
        #加载编译器 arm
        cmake['COMPILER'] = '\n# arm-none-eabi- must be part of path environment\n set(TOOLCHAIN_PREFIX   arm-none-eabi-)\n '
        cmake['COMPILER'] = cmake['COMPILER'] +'set(CMAKE_C_COMPILER    ${TOOLCHAIN_PREFIX}gcc)\n set(CMAKE_ASM_COMPILER ${CMAKE_C_COMPILER})\n set(CMAKE_CXX_COMPILER  ${TOOLCHAIN_PREFIX}g++) ' 
        cmake['COMPILER'] = cmake['COMPILER'] +'set(CMAKE_LINKER    ${TOOLCHAIN_PREFIX}g++)\n set(CMAKE_OBJCOPY ${TOOLCHAIN_PREFIX}objcopy)\n set(CMAKE_SIZE    ${TOOLCHAIN_PREFIX}size)\n'
        #配置内核型号
        cmake['CpuType'] =' # MCU specific flags\n set(TARGET_FLAGS "' + core +'")\n'
        #配置手动添加的编译选项
        cmake['CMAKE_C_FLAGS_MANUAL'] = '# This time, new compilation options have been added.\n #此处应该读取 手动配置的 CMAKE编译选项\n set(CMAKE_C_FLAGS_MANUAL '+self.Cmake['CMAKE_C_FLAGS_MANUAL']+')'
        #手动配置对应的链接文件 末尾以 .ld结尾 STM32的可以使用CudeMX生成，添加文件路径格式 应该类似与 下面的 inc与src
        cmake['CMAKE_LINKER_FILE'] = '#手动配置对应的链接文件 末尾以 .ld结尾 STM32的可以使用CudeMX生成,添加文件路径格式 应该类似与 下面的 inc与src\n set(CMAKE_LINKER_FILE '+self.Cmake['CMAKE_LINKER_FILE']+')'
        #配置配置通用的编译选项 等
        cmake['CMAKE_C_FLAGS'] = '\n\n# 此处是通用的编译选项C语言 自动生成\n set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${TARGET_FLAGS} ${CMAKE_C_FLAGS_MANUAL} -mthumb' \
        ' -Wall -fdata-sections -ffunction-sections -std=c99 -fno-rtti")'
        cmake['CMAKE_ASM_FLAGS'] = '# 此处是通用的编译选项汇编语言 自动生成\n set(CMAKE_ASM_FLAGS "${TARGET_FLAGS} -x -mthumb assembler-with-cpp -MMD -MP")'
        cmake['CMAKE_CXX_FLAGS']='# 此处是通用的编译选项CXX语言 自动生成\n set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -Wall -fdata-sections -ffunction-sections")\n\n'
        #配置宏定义
        cmake['defines'] = '#此处是项目使用的宏定义 自动生成\nadd_compile_definitions( \n'
        for define in self.project['defs']:
            cmake['defines']=cmake['defines']+'  '+define+'\n'
        cmake['defines']=cmake['defines'] + ')\n'
        #配置连接文件


        cmake['incs'] = '#generated include paths \n set(Inc_Pro \n'
        for inc in self.project['incs']:    
            inc_file = process_relative_path(inc)
            cmake['incs'] = cmake['incs'] + '   ${CMAKE_CURRENT_SOURCE_DIR}'+ inc_file + '\n'
            #cmake['incs'].append(inc_file)    
            #print(inc_file)
        cmake['incs'] = cmake['incs'] +  ')' + '\n'
        cmake['srcs'] = '#generated src paths \n set(SRC_Pro \n'



        for file in self.project['srcs']:
            src_file = process_relative_path(file)
            #print(src_file)
            if src_file.endswith('.c') or src_file.endswith('.h') or src_file.endswith('.cpp'):
                cmake['srcs'] = cmake['srcs'] + '   ${CMAKE_CURRENT_SOURCE_DIR}'+src_file+'\n'
                #cmake['files'].append({'path': src_file,'var':'SRC_FILE' + str(i)})  
        cmake['srcs'] = cmake['srcs'] +')\n'
        self.context['cmake'] = cmake
        
        abspath = os.path.abspath(os.path.join(self.path,'CMakeLists.txt'))
        self.generateFile()
        #

        print ('Created file CMakeLists.txt [{}]'.format(abspath))
        
#    def generateFile (self, pathSrc, pathDst='', author='Pegasus', version='v1.0.0', licence='licence.txt', template_dir='../PegasusTemplates'):
    def generateFile (self):
        cmake_file = self.path
        cmake_file_name = self.project['name'].text + ".cmake"

        context= self.context_to_text()
        context_str = context.strip('"\'')

        #context_str = "cmake_minimum_required(VERSION 3.22)"
        #print(context_str)
        safe_create_file_structure(cmake_file,"cmake",cmake_file_name,True,context_str)


    
    def CmakeCopyList(self):
        source_path = os.getcwd()
        source_path = Path(source_path)
        source_file = Path(source_path/"ProjectToCMAKE"/"cmake.cmake")
        parent_dir = Path(__file__).parent.parent.absolute()

        target_file = parent_dir/"CMakeLists.txt"

        source_file = Path(source_file)
        target_file = Path(target_file)
        copy_file_with_custom_name(source_file,target_file)
        return
        
    def context_to_text(self):
        """
        将 context 字典转换为自定义文本格式
        """
        lines = []
        
        def process_dict(d, indent=0):
            for key, value in d.items():
                if isinstance(value, dict):
                    lines.append("  " * indent + f"")
                    process_dict(value, indent + 1)
                elif isinstance(value, list):
                    lines.append("  " * indent + f"")
                    for item in value:
                        lines.append("  " * (indent + 1) + f"- {item}")
                else:
                    lines.append("  " * indent + f" {value}")
        
        process_dict(self.context['cmake'])
        #print(lines)
        return '\n'.join(lines)
    
    def copy_file_with_custom_name(source_file, target_file):
        """
    跨平台复制文件到指定路径（可自定义文件名）
    不存在则创建目录，存在则覆盖文件
    
    Args:
        source_file: 源文件路径
        target_file: 目标文件路径（可包含自定义文件名）
        """
        # 转换为 Path 对象（自动处理不同操作系统的路径分隔符）
        source = Path(source_file)
        target = Path(target_file)
        
        # 检查源文件是否存在
        if not source.exists():
            print("源文件不存在: {source}")
        
        # 确保目标目录存在
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制文件（自动覆盖已存在的文件）
        shutil.copy2(source, target)
        
        print("✅ 文件复制成功: {source} -> {target}")
        return True
        
