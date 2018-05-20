## 编译 CEF

### 准备目录和文件

创建下面目录

    c:\code\automate
    c:\code\chromium_git

下载[depot_tools](https://storage.googleapis.com/chrome-infra/depot_tools.zip)并解压到`c:\code\depot_tools`

更新 `depot_tools`

    cd c:\code\depot_tools
    update_depot_tools.bat

将`c:\code\depot_tools`添加到PATH环境变量中（如果本机同时拥有chromium编译环境，请注意调整环境变量的位置）

下载[automate-git.py](https://bitbucket.org/chromiumembedded/cef/raw/master/tools/automate/automate-git.py)到`c:\code\automate\automate-git.py`中

创建`c:\code\chromium_git\update.bat`文件

    set CEF_USE_GN=1
    set GN_DEFINES=use_jumbo_build=true enable_precompiled_headers=false
    set GN_ARGUMENTS=--ide=vs2017 --sln=cef --filters=//cef/*
    python ..\automate\automate-git.py --download-dir=c:\code\chromium_git --depot-tools-dir=c:\code\depot_tools --no-distrib --no-build

### 下载源码

运行`update.bat`文件下载`cef`和`chromium`源码，在这个过程中，`cef`源码会被首先下载到`c:\code\chromium_git\cef`目录，之后会被拷贝到`c:\code\chromium_git\chromium\src\cef`目录

    cd c:\code\chromium_git
    update.bat

### 创建编译目录

创建`c:\code\chromium_git\chromium\src\cef\create.bat`文件

    set CEF_USE_GN=1
    set GN_DEFINES=use_jumbo_build=true enable_precompiled_headers=false
    set GN_ARGUMENTS=--ide=vs2017 --sln=cef --filters=//cef/*
    call cef_create_projects.bat

运行`create.bat`文件

    cd c:\code\chromium_git\chromium\src\cef
    create.bat

### 编译源码

执行`ninja`编译任务

    cd c:\code\chromium_git\chromium\src
    ninja -C out\Debug_GN_x86 cef

### 运行示例程序

    cd c:\code\chromium_git\chromium\src
    out\Debug_GN_x86\cefclient.exe
