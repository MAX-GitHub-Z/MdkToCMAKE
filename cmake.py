# -*- coding: utf-8 -*-

import os
import platform
import datetime
from pathlib import Path
import json


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


    def populateCMake (self):
        """ Generate CMakeList.txt file for building the project
        """

        # For debug run cmake -DCMAKE_BUILD_TYPE=Debug or Release
        cmake = {}
        #fpu = '-mfpu=fpv5-sp-d16 -mfloat-abi=softfp'
        fpu = ''
        core = ""
        core = "-mcpu="+self.project['AdsCpuType'].lower()
        print("当前生成项目使用的 处理器内核为："+core)

        cmake['version'] = 'cmake_minimum_required(VERSION 3.1)'
        cmake['language'] =  '# Enable CMake support for ASM and C languages \n enable_language(C ASM)'
        cmake['project'] = '# Set the project name \n set(CMAKE_PROJECT_NAME '+self.project['name'] +')'






        cmake['incs'] = '#generated include paths \n set(Inc_Pro \n'
        for inc in self.project['incs']:    
            inc_file = process_relative_path(inc)
            cmake['incs'] = cmake['incs'] + '   ${CMAKE_CURRENT_SOURCE_DIR}'+ inc_file + '\n'
            #cmake['incs'].append(inc_file)    
            print(inc_file)
        cmake['incs'] = cmake['incs'] +  ')' + '\n'
        cmake['srcs'] = '#generated include paths \n set(SRC_Pro \n'


        cmake['files']=[]
        cmake['ass']=[]
        
        for file in self.project['srcs']:
            src_file = process_relative_path(file)
            #print(src_file)
            if src_file.endswith('.c') or src_file.endswith('.h') or src_file.endswith('.cpp'):
                cmake['srcs'] = cmake['srcs'] + '   ${CMAKE_CURRENT_SOURCE_DIR}'+src_file+'\n'
                #cmake['files'].append({'path': src_file,'var':'SRC_FILE' + str(i)})  

            
		
        cmake['cxx'] = 'false'
        
        cmake['c_flags'] = '-g -Wextra -Wshadow -Wimplicit-function-declaration -Wredundant-decls -Wmissing-prototypes -Wstrict-prototypes -fno-common -ffunction-sections -fdata-sections -MD -Wall -Wundef -mthumb ' + core + ' ' + fpu

        cmake['cxx_flags'] = '-Wextra -Wshadow -Wredundant-decls  -Weffc++ -fno-common -ffunction-sections -fdata-sections -MD -Wall -Wundef -mthumb ' + core + ' ' + fpu
 
        cmake['asm_flags'] = '-g -mthumb ' + core + ' ' + fpu #+ ' -x assembler-with-cpp'
        cmake['linker_flags'] = '-g -Wl,--gc-sections -Wl,-Map=' + cmake['project'] + '.map -mthumb ' + core + ' ' + fpu
        cmake['linker_script'] = 'STM32FLASH.ld'
        cmake['linker_path'] = ''  
   
        #self.linkerScript('STM32FLASH.ld',os.path.join(self.path,'STM32FLASH.ld'))
        
        cmake['oocd_target'] = 'stm32f3x'
        cmake['defines'] = []
        for define in self.project['defs']:
            cmake['defines'].append(define)
            
        cmake['libs'] = []
        
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


    
    def linkerScript(self,pathSrc, pathDst='',template_dir='.'):
#    def linkerScript(self,pathSrc, pathDst='',template_dir='.../PegasusTemplates'):
                
        if (pathDst == ''):
            pathDst = pathSrc
            
        self.context['file'] = os.path.basename(str(pathSrc))
        self.context['flash'] = '64'
        self.context['ram'] = '8'        
        
        env = Environment(loader=FileSystemLoader(template_dir),trim_blocks=True,lstrip_blocks=True)
        template = env.get_template(str(pathSrc))
        
        generated_code = template.render(self.context)
            
        if platform.system() == 'Windows':    

            with open(pathDst, 'w') as f:
                f.write(generated_code)
        
        elif platform.system() == 'Linux':

            with open(pathDst, 'w') as f:
                f.write(generated_code)        
        else:
            # Different OS than Windows or Linux            
            pass
        
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