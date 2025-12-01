#设置CMAKE 最低支持的版本
cmake_minimum_required(VERSION 3.20)

#CMAKE 交叉编译配置
SET(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR ARM)

# --- 警告：此操作会强制删除目录 ---
# 在配置开始时，如果存在名为 "build" 的目录，则删除它
if(EXISTS "${CMAKE_SOURCE_DIR}/build/")
    message(STATUS "Removing old build directory...")
    file(REMOVE_RECURSE "${CMAKE_SOURCE_DIR}/build/")
endif()

include(cmake/Rule.cmake)
# 当不是用ARM嵌入式工具链编译时，才设置版本属性
if(NOT CMAKE_C_COMPILER_ID STREQUAL "GNU" OR NOT CMAKE_SYSTEM_NAME STREQUAL "Generic")
    # 或者更直接地，检查工具链前缀
    if(NOT CMAKE_C_COMPILER MATCHES "arm-none-eabi")
        set_target_properties(my_embedded_app PROPERTIES VERSION 1.0.0)
    endif()
endif()


 # Set the project name 
set(CMAKE_PROJECT_NAME CMAKE)

project(${CMAKE_PROJECT_NAME} )

#set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
 # Enable CMake support for ASM and C languages 
 enable_language(C ASM)
 
#需要编译的.c文件
SET(SRC_LIST
    ${SRC_Pro}   
)

#编译时的头文件
include_directories(${Inc_Pro})
#编译成果物路径
set(OUTPUT_PAHT ${OutPut_Path})
set(EXECUTABLE_OUTPUT_PATH ${OUTPUT_PAHT})
set(CMAKE_EXE_LINKER_FLAGS ${LINKER_FLAGS})
add_executable(${CMAKE_PROJECT_NAME} ${SRC_LIST})
#强制输出的成果物为 .elf
set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".elf")
