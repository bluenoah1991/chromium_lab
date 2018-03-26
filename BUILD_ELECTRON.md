# 构建 *Electron*

## 下载 *electron* 项目源码

    git clone https://github.com/electron/electron.git

## 临时修改编译脚本 `script\bootstrap.py`

    def main():
      os.chdir(SOURCE_ROOT)

      args = parse_args()
      defines = args_to_defines(args)
      if not args.yes and PLATFORM != 'win32':
        check_root()
      if args.verbose:
        enable_verbose_mode()
      if sys.platform == 'cygwin':
        update_win32_python()

      update_submodules()
      return # 添加

## 执行编译脚本

    python script\bootstrap.py -v --target_arch=ia32 --build_debug_libcc

脚本运行会执行

    git submodule update --init --recursive

注意当 `//vendor/libchromiumcontent/vendor/depot_tools` 目录下载完毕后脚本结束

做下列修改

> //vendor/libchromiumcontent/vendor/depot_tools/bootstrap/win/get_file.js

    function Download(url, path, verbose) {
      if (verbose) {
        WScript.StdOut.Write(" *  GET " + url + "...");
      }
      try {
        xml_http = new ActiveXObject("MSXML2.ServerXMLHTTP");
        xml_http.setProxy(2, "127.0.0.1:8123", "127.0.0.1"); // 添加

注意当前版本的electron（[f993888](https://github.com/electron/electron/commit/f9938884248627335c59da6b3b0ff0dc7df3b258)）有如下编译Bug，需要修改`script\bootstrap.py`和`script\build-libchromiumcontent.py`文件

> https://github.com/electron/electron/pull/11927

如果需要生成VS工程文件，还需要修改

> //vendor/libchromiumcontent/script/lib/gn.py

    def generate(out_dir, chromium_root_dir, depot_tools_dir, env):
      executable = __get_executable_path(depot_tools_dir)
      out_dir_relative_path = os.path.relpath(out_dir, chromium_root_dir)
      subprocess.check_call([executable, 'gen', '--ide=vs', out_dir_relative_path],
                            cwd=chromium_root_dir, env=env)

如果使用预先下载的git cache目录，配置环境变量

    set LIBCHROMIUMCONTENT_GIT_CACHE=C:\libchromiumcontent_git_cache

取消对`script\bootstrap.py`文件的修改，并修改`vendor\libchromiumcontent\script\build-libchromiumcontent.py`文件

    def main():
      os.chdir(LIBCC_DIR)

      args = parse_args()
      if args.verbose:
        enable_verbose_mode()

      # ./script/bootstrap
      # ./script/update -t x64
      # ./script/build --no_shared_library -t x64
      # ./script/create-dist -c static_library -t x64 --no_zip
      script_dir = os.path.join(LIBCC_DIR, 'script')
      bootstrap = os.path.join(script_dir, 'bootstrap')
      update = os.path.join(script_dir, 'update')
      build = os.path.join(script_dir, 'build')
      create_dist = os.path.join(script_dir, 'create-dist')
      if args.force_update or libchromiumcontent_outdated():
        execute_stdout([sys.executable, bootstrap])
        execute_stdout([sys.executable, update, '-t', args.target_arch])
        update_gclient_done_marker()
      return # 添加

重新执行脚本会基于 *gclient* 工具下载 *chromium* 源码到 `//vendor/libchromiumcontent/src` 目录，待到下载完毕后脚本结束

这里有个Windows SDK版本问题，参考PR [error-c2371-client_id-redefinition-different-basic-types](https://github.com/codemeow5/chromium_lab/blob/master/TROUBLESHOOTING.md#error-c2371-client_id-redefinition-different-basic-types) 进行修改

取消`vendor\libchromiumcontent\script\build-libchromiumcontent.py`文件修改，重新执行脚本开始编译

待完毕后执行

    python script\bootstrap.py -v --target_arch=ia32 --msvs --build_debug_libcc

生成针对 *electron* 的 *Visual Studio* 工程文件

最后执行

    python script\build.py -c D

进行编译
