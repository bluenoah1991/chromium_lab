## 编译Omaha

参考文档

<https://github.com/google/omaha/blob/v1.3.34.7/doc/DeveloperSetupGuide.md>

前置条件

- Microsoft Visual Studio 2017 with Windows 10 SDK
- Python 2.7.x

获取源码

```
C:\src> git clone https://github.com/google/omaha.git
C:\src\omaha\> git checkout tags/v1.3.34.7 -b v1.3.34.7
```

下载[AtlServer.zip](http://atlserver.codeplex.com/)，将`AtlServer.zip\sourceCode\sourceCode.zip`中的内容拷贝到`C:\src\atl_server\files`目录下

下载[WTL10_8356.zip](http://sourceforge.net/projects/wtl/)，将`WTL10_8356.zip\`中的内容拷贝到`C:\src\wtl\files`目录下

下载[wix311.exe](http://wix.sourceforge.net/)，运行安装包并安装到默认位置

下载并安装[pywin32](https://github.com/mhammond/pywin32/releases/download/b224/pywin32-224.win-amd64-py2.7.exe)

下载[scons-1.3.1.zip](http://sourceforge.net/projects/scons/files/scons/1.3.1/)并解压到`C:\src\scons-1.3.1`目录下

下载[swtoolkit.0.9.1.zip](http://code.google.com/p/swtoolkit/)到`C:\src\swtoolkit`目录下

下载[go1.12.5.windows-amd64.msi](https://golang.org/dl/)，运行安装。

下载[protoc-3.8.0-rc-1-win32.zip](https://github.com/google/protobuf/releases)，并解压到`C:\protobuf`目录下，

下载[protobuf-cpp-3.8.0-rc-1.zip](https://github.com/google/protobuf/releases)，将`protobuf-cpp-3.8.0-rc-1.zip\protobuf-3.8.0-rc-1\src`解压到`C:\protobuf\src`目录下。

下载依赖的子仓库

```
C:\src\omaha\third_party> git clone https://chromium.googlesource.com/breakpad/breakpad
C:\src\omaha\third_party> git clone https://github.com/google/googletest.git
```

针对版本v1.3.34.7，缺少libzip和zlib相关文档，请查看[Issue](<https://github.com/google/omaha/pull/149/files>)，以及<https://github.com/google/omaha/commit/03e83a66d524157242380a8e690b62d04a456062>

下载[libzip-1.3.0.tar.gz](https://libzip.org/download/libzip-1.3.0.tar.gz)，并将`libzip-1.3.0.tar.gz\libzip-1.3.0.tar\libzip-1.3.0\`拷贝到`C:\src\omaha\third_party\libzip`目录下

下载[zlib-1.2.11.tar.gz](https://zlib.net/zlib-1.2.11.tar.gz)，并将`zlib-1.2.11.tar.gz\zlib-1.2.11.tar\zlib-1.2.11\`拷贝到`C:\src\omaha\third_party\zlib\v1_2_11`目录下

从[<https://cygwin.com/install.html>](<https://cygwin.com/install.html>)下载`setup-x86_64.exe`，并安装Cygwin。在安装过程中选择安装`make`工具链。

运行Cygwin Terminal，跳转到`C:\src\omaha\third_party\zlib\v1_2_11`目录下，运行

```
C:\src\omaha\third_party\zlib\v1_2_11> mkdir build
C:\src\omaha\third_party\zlib\v1_2_11> cd build
C:\src\omaha\third_party\zlib\v1_2_11\build> cmake ..
```

运行Cygwin Terminal，跳转到`C:\src\omaha\third_party\libzip`目录下，运行

```
C:\src\omaha\third_party\libzip> mkdir build
C:\src\omaha\third_party\libzip> cd build
C:\src\omaha\third_party\libzip> cmake ..
```

修改头文件引用

C:\src\omaha\third_party\zlib\v1_2_11\zlib.h

```
#ifndef ZLIB_H
#define ZLIB_H

#include "build\zconf.h"

#ifdef __cplusplus
extern "C" {
#endif
```

C:\src\omaha\third_party\libzip\lib\zip.h

```
#ifdef __cplusplus
extern "C" {
#if 0
} /* fix autoindent */
#endif
#endif

#include "..\build\zipconf.h"

#include <sys/types.h>
#include <stdio.h>
#include <time.h>
```

修改文件，确保Go编译时获取到正确的`LocalAppData`环境变量。

C:\src\omaha\omaha\site_scons\site_tools\omaha_builders.py

```
def OmahaCertificateTagExe(env, target, source):
  """Adds a superfluous certificate with a magic signature to an EXE. The file
  must be signed with Authenticode in order for Certificate Tagging to succeed.

  Args:
    env: The environment.
    target: Name of the certificate-tagged file.
    source: Name of the file to be certificate-tagged.

  Returns:
    Output node list from env.Command().
  """

  certificate_tag = ('"' + env['ENV']['GOROOT'] + '/bin/go.exe' + '"' +
      ' run $MAIN_DIR/../common/certificate_tag/certificate_tag.go')
  magic_bytes = 'Gact2.0Omaha'
  padded_length = len(magic_bytes) + 2 + 8192
  env['ENV']['LocalAppData'] = os.getenv('LocalAppData') # Pass environment variable 'LocalAppData' to 'env'
  certificate_tag_cmd = env.Command(
      target=target,
      source=source,
      action=certificate_tag +
             ' -set-superfluous-cert-tag=' + magic_bytes +
             ' -padded-length=' + str(padded_length) + ' -out $TARGET $SOURCE',
  )

  return certificate_tag_cmd
```

使用文本编辑器打开`C:\src\omaha\omaha\hammer.bat`，并修改`:set_env_variables`节

```
:set_env_variables

:: Change these variables to match the local build environment.

:: Directory where the Go programming language toolchain is installed.
set GOROOT=C:\Go

:: Directory where AtlServer files are.
set OMAHA_ATL_SERVER_DIR=C:\src\atl_server\files

:: This will depend on your OS. If this version of the .Net framework came with
:: the OS, then set it to the framework directory
:: (something like C:\Windows\Microsoft.NET\Framework\v2.0.50727).
:: Otherwise, set it to the directory where the .NET framework is installed.
set OMAHA_NET_DIR=%WINDIR%\Microsoft.NET\Framework\v2.0.50727

:: This directory is needed to find mage.exe tool, which is the .Net manifest
:: generating tool. This tool ships as part of the Windows SDK.
:: However, newer versions of mage.exe can't targer older versions of .Net
:: framework. If there is a need for the click-once application to run on older
:: versions of the .Net framework, then an older version of the Windows SDK
:: needs to be installed and this environment variable point to that directory.
set OMAHA_NETFX_TOOLS_DIR=%WindowsSDK_ExecutablePath_x86%

:: This directory is needed to find protoc.exe, which is the protocol buffer
:: compiler. From the release page https://github.com/google/protobuf/releases,
:: download the zip file protoc-$VERSION-win32.zip. It contains the protoc
:: binary. Unzip the contents under C:\protobuf.
set OMAHA_PROTOBUF_BIN_DIR=C:\protobuf\bin

:: This directory is needed to find the protocol buffer source files. From the
:: release page https://github.com/google/protobuf/releases, download the zip
:: file protobuf-cpp-$VERSION.zip. Unzip the "src" sub-directory contents to
:: C:\protobuf\src.
set OMAHA_PROTOBUF_SRC_DIR=C:\protobuf\src

:: Directory where Python (python.exe) is installed.
set OMAHA_PYTHON_DIR=C:\Python27

:: Directory in WiX where candle.exe and light.exe are installed.
set OMAHA_WIX_DIR=%ProgramFiles(x86)%\WiX Toolset v3.11\bin

:: Root directory of the WTL installation.
set OMAHA_WTL_DIR=C:\src\wtl\files

set OMAHA_PLATFORM_SDK_DIR=%WindowsSdkDir%\
set OMAHA_WINDOWS_SDK_10_0_VERSION=%WindowsSDKVersion:~0,-1%

:: Directory which includes the sign.exe tool for Authenticode signing.
set OMAHA_SIGNTOOL_SDK_DIR=%WindowsSdkDir%bin\10.0.17763.0\x86
set PYTHONPATH=%OMAHA_PYTHON_DIR%

:: Directory of Scons (http://www.scons.org/).
set SCONS_DIR=C:\src\scons-1.3.1\engine

:: Directory of the Google's Software Construction Toolkit.
set SCT_DIR=C:\src\swtoolkit

set PROXY_CLSID_TARGET=%~dp0proxy_clsids.txt
set CUSTOMIZATION_UT_TARGET=%~dp0common\omaha_customization_proxy_clsid.h

rem Force Hammer to use Python 2.7
set PYTHON_TO_USE=python_27
call "%SCT_DIR%\hammer.bat" %*

if /i {%1} == {-c} (
  del /q /f "%PROXY_CLSID_TARGET%" 2> NUL
  del /q /f "%CUSTOMIZATION_UT_TARGET%" 2> NUL
)

goto end
```

使用管理员权限打开新的命令提示符窗口，跳转到`C:\src\omaha\omaha`目录，执行

```
C:\src\omaha\omaha> "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvarsamd64_x86.bat"
```

配置对应的VisualStudio工具链环境变量，然后执行

```
C:\src\omaha\omaha> hammer
```

开始构建