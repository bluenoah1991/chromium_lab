# 编译 *Chromium*

## 前置条件

安装 *Python 2.7* 和 *Git*

安装 *[pywin32](https://github.com/mhammond/pywin32/releases)* ( [libchromiumcontent](https://github.com/electron/libchromiumcontent) 项目的安装前置条件中也提到了这一部分)

安装 *Visual Studio 2017*，勾选 *Desktop development with C++*，*Windows 10 SDK 10.0.15063* 和 *MFC and ATL support* 组件  
待安装完毕后，在

> Control Panel → Programs → Programs and Features → Select the “Windows Software Development Kit” → Change → Change → Check “Debugging Tools For Windows” → Change

检查当前代码的下列位置

https://cs.chromium.org/chromium/src/build/toolchain/win/setup_toolchain.py?q=15063&sq=package:chromium&dr=C&l=152

当前版本中，`10.0.16299.0`的Windows SDK存在不兼容问题，脚本强制使用`10.0.15063`版本

下载[depot_tools](https://storage.googleapis.com/chrome-infra/depot_tools.zip)并解压到C盘根目录

将`C:\depot_tools`添加到PATH环境变量中，注意需要将其放置在Python路径前面，同时设置环境变量`DEPOT_TOOLS_WIN_TOOLCHAIN`为`0`

## 相关环境变量

| ENV | DESC | File |
| --- | ---- | ---- |
| GYP_MSVS_OVERRIDE_PATH | 基于该路径查找*vcvarsall.bat*文件，设置VS相关环境变量 | //src/build/toolchain/win/setup_toolchain.py |
| GYP_MSVS_VERSION | 指定当前使用的MSVS工具链版本，默认是*2017* | //src/build/vs_toolchain.py |

## 首次运行 *gclient* 更新 *depot_tools*

在任意位置运行命令

    gclient

完毕后，运行命令

    where python

确保显示下列输出

    C:\depot_tools\python.bat
    C:\Python27\python.exe

## 配置Git

    $ git config --global user.name "My Name"
    $ git config --global user.email "my-name@chromium.org"
    $ git config --global core.autocrlf false
    $ git config --global core.filemode false
    $ git config --global branch.autosetuprebase always

## 拷贝 *git cache*

将之前准备的 *git cache* 拷贝并解压到`C:\chromium_git_cache`目录，并配置环境变量

    set GCLIENT_CACHE_DIR=C:\chromium_git_cache

## 获取 *chromium* 代码

创建`C:\chromium`目录，进入目录并运行

    fetch chromium

待下载完毕后进入`C:\chromium\src`目录并运行

    gn gen --ide=vs out\Default --args="is_component_build = true enable_nacl = false target_cpu = \"x86\""

## 编译代码

在`C:\chromium\src`目录运行

    ninja -C out\Default chrome

待编译完成后，启动`out\Default\chrome.exe`
