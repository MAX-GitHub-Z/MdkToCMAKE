# -*- coding: utf-8 -*-

""" 解析UVPROJX项目格式文件的类
    需要将该工程放到项目目录的最外层的 ProjectToCMAKE 目录下运行
    该类使用lxml库进行XML解析，因此需要确保环境中已安装lxml库。
    该库的目的是解析MKD的UVPROJX项目文件，并提取项目的相关设置，如项目名称、芯片型号、包含路径、宏定义和源文件列表。
    @file
"""

import os
from lxml import objectify
from pathlib import Path

class UVPROJXProject(object):
    """ Class for converting UVPROJX project format file
    """

    def __init__(self, path, xmlFile):
        self.path = path
        self.project = {}
        self.xmlFile = xmlFile
        xmltree = objectify.parse(xmlFile)
        self.root = xmltree.getroot()


    def parseProject(self):
        """ Parses EWP project file for project settings
        """



        self.project['name'] = self.root.Targets.Target.TargetName
        self.project['chip'] = str(self.root.Targets.Target.TargetOption.TargetCommonOption.Device)
        self.project['Vendor'] = str(self.root.Targets.Target.TargetOption.TargetCommonOption.Vendor)
        self.project['FlashUtilSpec'] = str(self.root.Targets.Target.TargetOption.TargetCommonOption.Cpu)
        self.project['AdsCpuType'] = self.root.Targets.Target.TargetOption.TargetArmAds.ArmAdsMisc.AdsCpuType.text
        #self.project['Define']=str(self.root.Targets.Target.TargetOption.TargetArmAds.VariousControls.Define)
        self.project['incs'] = self.root.Targets.Target.TargetOption.TargetArmAds.Cads.VariousControls.IncludePath.text.split(';')
        self.project['mems'] = self.root.Targets.Target.TargetOption.TargetCommonOption.Cpu
        self.project['defs'] = self.root.Targets.Target.TargetOption.TargetArmAds.Cads.VariousControls.Define.text.split(',')
        #print(self.project['FlashUtilSpec'])
        #print(self.project['AdsCpuType'],self.project['defs'] )
        #print(self.project['incs'])
        self.project['srcs'] = []

        #print(self.project['name'],self.project['chip'],self.project['Vendor'],self.project['FlashUtilSpec'])

        for element in self.root.Targets.Target.Groups.getchildren():
            #print('GroupName: ' + element.GroupName.text)
            if hasattr(element, 'Files'):
                for file in element.Files.getchildren():
                    if not str(file.FilePath.text).endswith('.s'):
                        s = str(file.FilePath.text)
                        src_file=Path(s)
                        #print(src_file)
                        #使用标准化的路径 
                        self.project['srcs'].append(src_file)

        for i in range(0, len(self.project['incs'])):
            s = str(self.project['incs'][i])
            src_file=Path(s)
            #print(src_file)
            self.project['incs'][i] = src_file

        self.project['files'] = []
        i = 0

        """增加在不同编译器下 需要增加的启动文件
        """
        """
        if os.path.exists(self.path + '/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/gcc'):
            for entry in os.listdir(self.path + '/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/gcc'):
                if entry.endswith('.S') or entry.endswith('.s'):
                    self.project['files'].append(self.path + '/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/gcc/'+ entry)
        """

    def displaySummary(self):
        """ Display summary of parsed project settings
        """
        print('Project Name:' + self.project['name'])
        print('Project chip:' + self.project['chip'])
        print('Project includes: ' + ' '.join(self.project['incs']))
        print('Project defines: ' + ' '.join(self.project['defs']))
        print('Project srcs: ' + ' '.join(self.project['srcs']))
        print('Project: ' + self.project['mems'])

    def getProject(self):
        """ Return parsed project settings stored as dictionary
        @return Dictionary containing project settings
        """
        return self.project




