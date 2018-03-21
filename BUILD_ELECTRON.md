# 构建 *Electron*

## 下载 *electron* 项目源码

    git clone https://github.com/electron/electron.git

## 执行编译脚本

    python script\bootstrap.py -v --target_arch=ia32 --build_debug_libcc

注意当前版本的electron有如下编译Bug

> https://github.com/electron/electron/pull/11927

脚本运行前期会执行

    git submodule update --init --recursive

注意当 `//vendor/libchromiumcontent/vendor/depot_tools` 目录下载完毕后取消脚本

做下列修改

> //vendor/libchromiumcontent/vendor/depot_tools/bootstrap/win/get_file.js

    function Download(url, path, verbose) {
      if (verbose) {
        WScript.StdOut.Write(" *  GET " + url + "...");
      }
      try {
        xml_http = new ActiveXObject("MSXML2.ServerXMLHTTP");
        xml_http.setProxy(2, "127.0.0.1:8123", "127.0.0.1"); // 添加

重新执行脚本会基于 *gclient* 工具下载 *chromium* 源码到 `//vendor/libchromiumcontent/src` 目录，待到下载完毕后，取消脚本

参考问题 [error-c2371-client_id-redefinition-different-basic-types](https://github.com/codemeow5/chromium_lab/blob/master/TROUBLESHOOTING.md#error-c2371-client_id-redefinition-different-basic-types) 进行修改  

重新执行脚本，待完毕后执行

    python script\bootstrap.py -v --target_arch=ia32 --msvs --build_debug_libcc

生成 *Visual Studio* 工程文件

最后执行

    python script\build.py -c D

进行编译
