<!-- [中文](./Doc/zh/README_zh.md) | [English](./Doc/en/README_en.md) -->

<div align="center">

  <!-- 动态宽度分隔线 -->
  
 <!-- <img src="./Doc/Micor_DAPLink_log2.png" width="100%"> -->
  
   <!-- ![Micor_DAPLink_Log](./Doc/Micor_DAPLink_log.png)-->
  <!-- 主标题 -->
  <h1>
     <!-- <img src="assets/rocket.png" width="40"> -->
    <span style="color: #ff6b6b">ProjectToCMAKE</span>
    <span style="color: #4ecdc4">CMAKE</span>
    <!-- <img src="assets/rocket.png" width="40"> -->
  </h1>
  
  <!-- 副标题 -->
  <h3>MDK转CMAKE</h3>
  
  <!-- 徽章区 -->
  <p>
  
[![Latest Release](https://img.shields.io/github/v/release/ProjectToCMAKE/ProjectToCMAKE?include_prereleases&label=最新版本&logo=github&logoColor=white)](https://github.com/ProjectToCMAKE/DAPLink_Box/releases) 
[![Release Date](https://img.shields.io/github/release-date/ProjectToCMAKE/DAPLink_Box?include_prereleases&label=发布时间&logo=github&logoColor=white)](https://github.com/ProjectToCMAKE/DAPLink_Box/releases)
[![GitHub License](https://img.shields.io/github/license/ProjectToCMAKE/DAPLink_Box?color=blue&logo=github&logoColor=white)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/ProjectToCMAKE/DAPLink_Box/total?logo=github&logoColor=white)](https://github.com/ProjectToCMAKE/DAPLink_Box/releases)

  </p>
  
  <!-- 按钮区 -->
   <!-- 目前不需要 暂不添加
  <p>
    [![Open in GitHub](https://img.shields.io/badge/View-GitHub-black?logo=github&style=flat-square)](https://github.com/username/repo)
    [![Download ZIP](https://img.shields.io/badge/Download-ZIP-blue?style=flat-square)](https://github.com/username/repo/archive/refs/heads/main.zip)
  </p>
   -->
  <!-- 动态宽度分隔线 -->
<!--  <img src="https://user-images.githubusercontent.com/.../bottom-bar.svg" width="100%"> -->
</div>

# 项目简介

这个项目的目标是将KEIL上的MDK方便的移植道GCC上，便于多平台开发等

目前已实现功能

1、支持将MDK转换为CMKE，仅同时支持一个项目进行配置，

2、仅支持转换后在VSCODE上进行编译，支持STM32cude插件（不使用默认配置，仅使用CMAKE工具进行编译与调试）


# TODO

1、支持命令行CMAKE  .编译

2、写使用说明与相关教程


4、同时支持多个项目

5、使用QT写一个转换工具 .exe（最终目标 看情况是否可以完成）

# 关键字

KEIL CMAKE MDK STM32 GD32