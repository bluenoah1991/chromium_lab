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

## 离线安装 *Visual Studio 2017*

    C:\>vs_Enterprise.exe --layout c:\vs2017layout --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Component.VC.ATLMFC --add Microsoft.VisualStudio.Component.Windows10SDK.15063.Desktop --add Microsoft.VisualStudio.Component.VC.140 --includeRecommended --lang en-US
    
    C:\vs2017layout>vs_Enterprise.exe --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Component.VC.ATLMFC --add Microsoft.VisualStudio.Component.Windows10SDK.15063.Desktop --add Microsoft.VisualStudio.Component.VC.140 --includeRecommended

参考

> https://docs.microsoft.com/en-us/visualstudio/install/install-vs-inconsistent-quality-network
> https://docs.microsoft.com/en-us/visualstudio/install/workload-component-id-vs-enterprise

## 相关环境变量

| ENV | DESC | File |
| --- | ---- | ---- |
| GYP_MSVS_OVERRIDE_PATH | 基于该路径查找*vcvarsall.bat*文件，设置VS相关环境变量 | //src/build/toolchain/win/setup_toolchain.py |
| GYP_MSVS_VERSION | 指定当前使用的MSVS工具链版本，默认是*2017* | //src/build/vs_toolchain.py |
| gn gen --ide | 指定生成的VS解决方案版本，默认是*vs2017* | https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/reference.md#gen |

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

或者

    gn gen --ide=vs out\default_release_x86 --args="is_debug = false is_component_build = false enable_nacl = false target_cpu = \"x86\""

## 获取指定版本源码

创建`C:\chromium`目录，进入目录并运行

    gclient config https://chromium.googlesource.com/chromium/src.git

`gclient`不会接受`GCLIENT_CACHE_DIR`环境变量，所以你需要额外指定你的缓存目录

    gclient config --cache-dir C:\chromium_git_cache https://chromium.googlesource.com/chromium/src.git

这将生成一个`.gclient`文件，注意检查`.gclient`中的`cache_dir`属性，然后运行

    gclient sync --revision src@{rev} --with_tags --with_branch_heads

例如获取 67.0.3396.87 版本源码

    gclient sync --revision src@67.0.3396.87 --with_tags --with_branch_heads

## 编译代码

在`C:\chromium\src`目录运行

    ninja -C out\Default chrome

待编译完成后，启动`out\Default\chrome.exe`

## 更新代码

对于有改动的仓库，使用

    git rebase-update  

进行更新，如果进入 *mid-rebase* 状态，请手工解决冲突，并重新运行命令。然后使用

    gclient sync  

更新整个源码树

