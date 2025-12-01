# -*- coding: utf-8 -*-

import os
from pathlib import Path
import tempfile
import shutil

def safe_create_file_structure(base_dir, file_name,file_cover = False, content="",indent=0):
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
        folder_path = Path(base_dir)
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
    
    return str(processed_path)

def read_file_with_line_numbers(filename, encoding='utf-8'):
    """
    读取文件内容并按行分隔，返回带行号的内容列表
    
    参数:
    filename: 文件名
    encoding: 文件编码，默认为utf-8
    
    返回:
    list: 包含行号和内容的元组列表 [(行号, 内容)]
    """
    try:
        with open(filename, 'r', encoding=encoding) as file:
            lines = file.readlines()
        
        # 返回带行号的内容列表（行号从1开始）
        return [(i+1, line.rstrip('\n\r')) for i, line in enumerate(lines)]
    
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在")
        return []
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return []
def write_file_with_modifications(filename, modified_data, encoding='utf-8'):
    """
    将修改后的数据写入文件（跨平台兼容）
    
    参数:
    filename: 文件名
    modified_data: 修改后的数据，可以是字符串列表或带行号的元组列表
    encoding: 文件编码，默认为utf-8
    
    返回:
    bool: 操作是否成功
    """
    try:
        # 处理不同格式的输入数据
        if modified_data and isinstance(modified_data[0], tuple):
            # 如果是带行号的元组列表，提取内容部分
            lines = [line for _, line in modified_data]
        else:
            lines = modified_data
        
        # 使用临时文件确保写入安全
        with tempfile.NamedTemporaryFile(
            mode='w', 
            encoding=encoding, 
            delete=False,
            newline=''  # 使用系统默认换行符
        ) as temp_file:
            
            # 写入数据，使用系统默认换行符
            for line in lines:
                temp_file.write(line + '\n')
        
        # 用临时文件替换原文件
        shutil.move(temp_file.name, filename)
        
        print(f"成功写入文件: {filename}")
        return True
    except Exception as e:
        print(f"写入文件时发生错误：{e}")
        # 清理临时文件
        if 'temp_file' in locals() and os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        return False
    
def are_first_n_chars_equal(str1, str2, n):
    """
    判断两个字符串的前n个字符是否相同
    
    参数:
    str1: 第一个字符串
    str2: 第二个字符串
    n: 要比较的字符数量
    
    返回:
    bool: 如果前n个字符相同返回True，否则返回False
    """
    # 处理边界情况
    if n < 0:
        raise ValueError("n不能为负数")
    
    # 如果n为0，总是返回True（比较0个字符）
    if n == 0:
        return True
    
    # 如果任一字符串长度小于n，无法比较
    if len(str1) < n or len(str2) < n:
        return False
    
    # 比较前n个字符
    return str1[:n] == str2[:n]

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
        #safe_create_file_structure(cmake_file, "cmake", cmake_file_name)
        #此处应该读取 手动配置的 CMAKE编译选项
        self.Cmake['CMAKE_C_FLAGS_MANUAL']= ''
        self.Cmake['CMAKE_LINKER_FILE'] = ''
        self.Cmake['CMAKE_SRC_INIT']=''

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

        cmake['version'] = 'cmake_minimum_required(VERSION 3.20)'
        #cmake['language'] =  '# Enable CMake support for ASM and C languages \n enable_language(C ASM)'
        cmake['CMAKE_SYSTEM'] = 'set(CMAKE_SYSTEM_NAME Generic)\n set(CMAKE_SYSTEM_PROCESSOR arm)\n'
        cmake['project'] = '# Set the project name \n set(CMAKE_PROJECT_NAME '+self.project['name'] +')\n'

        #配置手动添加的编译选项
        cmake['CMAKE_C_FLAGS_MANUAL'] = '\n\n# This time, new compilation options have been added.\n #此处应该读取 手动配置的 CMAKE编译选项\n set(CMAKE_C_FLAGS_MANUAL '+self.Cmake['CMAKE_C_FLAGS_MANUAL']+')'
        #手动配置对应的链接文件 末尾以 .ld结尾 STM32的可以使用CudeMX生成，添加文件路径格式 应该类似与 下面的 inc与src
        cmake['CMAKE_LINKER_FILE'] = '#手动配置对应的链接文件 末尾以 .ld结尾 STM32的可以使用CudeMX生成,添加文件路径格式 应该类似与 下面的 inc与src\n #示例： ${CMAKE_CURRENT_SOURCE_DIR}/Drivers/CMSIS/Device/ST/STM32F1xx/STM32F103XX_FLASH.ld)\n' \
        'set(CMAKE_LINKER_FILE '+self.Cmake['CMAKE_LINKER_FILE']+')'
        #手动配置启动文件 asm文件 引导设备启动
        cmake['CMAKE_SRC_INIT']= '#手动配置启动文件 末尾以 .s/.S 结尾 STM32的可以使用CudeMX生成,添加文件路径格式 应该类似与 下面的 inc与src \n #示例：${CMAKE_CURRENT_SOURCE_DIR}/Drivers/CMSIS/Device/ST/STM32F1xx/Source/Templates/gcc/startup_stm32f103xb.s\n ' \
        'set(CMAKE_LINKER_FILE '+self.Cmake['CMAKE_SRC_INIT']+')'
        #手动配置gcc编译时的路径

        cmake['CMAKE_COMPILER_PATH'] = ' if(CMAKE_C_COMPILER)\n   message(STATUS "CMAKE_C_COMPILER: ${CMAKE_C_COMPILER}")\n    get_filename_component(ABS_CONFIG_DIR "${CMAKE_C_COMPILER}" DIRECTORY ABSOLUTE)\n'\
        '   message(STATUS "ABS_CONFIG_DIR: ${ABS_CONFIG_DIR}")\n    set(TOOLCHAIN_PREFIX ${ABS_CONFIG_DIR}/arm-none-eabi-)\n    message(STATUS "TOOLCHAIN_PREFIX: ${TOOLCHAIN_PREFIX}")\n'\
        '   set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PREFIX}g++.exe)\n endif()\n    set(CMAKE_ASM_COMPILER  ${CMAKE_C_COMPILER})\n    set(CMAKE_LINKER        ${CMAKE_CXX_COMPILER})\n'\
        '   set(CMAKE_OBJCOPY       ${TOOLCHAIN_PREFIX}objcopy.exe)\n    set(CMAKE_SIZE          ${TOOLCHAIN_PREFIX}size.exe)'
        #cmake['CMAKE_COMPILER_PATH'] = '# arm-none-eabi- must be part of path environment\n #手动配置启动文件 可以网上找教程 安装GCC编译工具链 并找到安装路径 举例: '\
        ' E:/gcc/10_2021.10/bin/arm-none-eabi- \nset(TOOLCHAIN_PREFIX   )\n '

        #加载编译器 arm
        #cmake['CMAKE_COMPILER'] = '\n\n set(CMAKE_C_COMPILER    ${TOOLCHAIN_PREFIX}gcc.exe)\n set(CMAKE_ASM_COMPILER ${CMAKE_C_COMPILER})\n set(CMAKE_CXX_COMPILER  ${TOOLCHAIN_PREFIX}gcc.exe) \n' 
        #cmake['CMAKE_COMPILER'] = cmake['CMAKE_COMPILER'] +'set(CMAKE_LINKER    ${TOOLCHAIN_PREFIX}gcc.exe)\n set(CMAKE_OBJCOPY ${TOOLCHAIN_PREFIX}objcopy.exe)\n set(CMAKE_SIZE    ${TOOLCHAIN_PREFIX}size.exe)\n'
        #配置内核型号
        cmake['CpuType'] =' # MCU specific flags\n set(TARGET_FLAGS "' + core +'")\n'
        #配置配置通用的编译选项 等
        cmake['CMAKE_C_FLAGS'] = '# 此处是通用的编译选项C语言 自动生成\n set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${TARGET_FLAGS} ${CMAKE_C_FLAGS_MANUAL} -mthumb' \
        ' -Wall -fdata-sections -ffunction-sections ")'
        cmake['CMAKE_ASM_FLAGS'] = '# 此处是通用的编译选项汇编语言 自动生成\n set(CMAKE_ASM_FLAGS "${TARGET_FLAGS} -x -mthumb assembler-with-cpp -MMD -MP")'
        cmake['CMAKE_CXX_FLAGS']='# 此处是通用的编译选项CXX语言 自动生成\n set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -Wall -fdata-sections -ffunction-sections")\n\n'
        cmake['CMAKE_C_FLAGS_INIT']='set(CMAKE_C_FLAGS_INIT "--specs=nano.specs --specs=nosys.specs -mfloat-abi=soft -mthumb")\n'
        #配置宏定义
        cmake['defines'] = '#此处是项目使用的宏定义 自动生成\nadd_compile_definitions( \n'
        for define in self.project['defs']:
            cmake['defines']=cmake['defines']+'  '+define+'\n'
        cmake['defines']=cmake['defines'] + ')\n'
        #配置连接文件output
        cmake['Link_Flags']='\n set(LINKER_FLAGS "-T${CMAKE_LINKER_FILE} --specs=nano.specs --specs=nosys.specs -mfloat-abi=soft -mthumb")'
        #配置成果物路径
        rlaease_path = Path(self.path/"release")
        path_obj = Path(rlaease_path)
        # 转换为字符串时会使用当前系统的分隔符，可以强制转换为POSIX格式
        posix_path = path_obj.as_posix()
        cmake['output'] = '#此处是项目的成果物输出路径 默认默认生成在父目录下/release/project_name中 如果需要修改 请在cmake.py中进行\nSET(OutPut_Path '+str(posix_path)+')\n'

        cmake['incs'] = '#generated include paths \n set(Inc_Pro \n'
        for inc in self.project['incs']:    
            inc_file = process_relative_path(inc)
            path_obj = Path(inc_file)
            # 转换为字符串时会使用当前系统的分隔符，可以强制转换为POSIX格式
            posix_path = path_obj.as_posix()
            cmake['incs'] = cmake['incs'] + '   ${CMAKE_CURRENT_SOURCE_DIR}/'+ posix_path + '\n'
            #cmake['incs'].append(inc_file)    
            #print(inc_file)
        cmake['incs'] = cmake['incs'] +  ')' + '\n'
        cmake['srcs'] = '#generated src paths \n set(SRC_Pro \n'



        for file in self.project['srcs']:
            src_file = process_relative_path(file)
            #print(src_file)
            if src_file.endswith('.c') or src_file.endswith('.h') or src_file.endswith('.cpp'):
                path_obj = Path(src_file)
                # 转换为字符串时会使用当前系统的分隔符，可以强制转换为POSIX格式
                posix_path = path_obj.as_posix()
                cmake['srcs'] = cmake['srcs'] + '   ${CMAKE_CURRENT_SOURCE_DIR}/'+posix_path+'\n'
                #cmake['files'].append({'path': src_file,'var':'SRC_FILE' + str(i)})  
        cmake['srcs'] = cmake['srcs'] +')\n'
        self.context['cmake'] = cmake
        
        #abspath = os.path.abspath(os.path.join(self.path,'CMakeLists.txt'))
        self.generateFile()
        #

        #print ('Created file CMakeLists.txt [{}]'.format(abspath))
        
#    def generateFile (self, pathSrc, pathDst='', author='Pegasus', version='v1.0.0', licence='licence.txt', template_dir='../PegasusTemplates'):
    def generateFile (self):
        cmake_file = Path(self.path/"cmake")
        cmake_file_name = self.project['name'].text + ".cmake"

        Str_file= self.context['cmake']
        context= self.context_to_text(Str_file)
        context_str = context.strip('"\'')

        safe_create_file_structure(cmake_file,cmake_file_name,True,context_str)


    
    def CmakeCopyList(self,ProjectName):
        print(ProjectName)
        source_path = os.getcwd()
        source_path = Path(source_path)
        source_file = Path(source_path/"ProjectToCMAKE"/"cmake.cmake")
        read_cmake=read_file_with_line_numbers(source_file)

        Set_Project_name = "set(CMAKE_PROJECT_NAME "+ProjectName+")\n"
        for  i, (num, line) in enumerate(read_cmake):
            #print(i,num,line)
            if are_first_n_chars_equal(line,Set_Project_name,22):
                modified_line = line.replace(line, Set_Project_name)
                read_cmake[i] = (num, modified_line)


        #print(read_cmake)
        parent_dir = Path(__file__).parent.parent.absolute()
        target_file = parent_dir/"CMakeLists.txt"

        source_file = Path(source_file)
        target_file = Path(target_file)
        #safe_create_file_structure(source_path,"CMakeLists.txt",True,context_str)
        copy_file_with_custom_name(source_file,target_file)
        write_file_with_modifications(target_file,read_cmake)
        return
        
    def context_to_text(self,ListDate):
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
        
        process_dict(ListDate)#self.context['cmake']
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
        
