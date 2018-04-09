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

注意当 `//vendor/libchromiumcontent` 目录下载完毕后脚本结束

为了生成VS工程文件，需要修改

> //vendor/libchromiumcontent/script/lib/gn.py

    def generate(out_dir, chromium_root_dir, depot_tools_dir, env):
      executable = __get_executable_path(depot_tools_dir)
      out_dir_relative_path = os.path.relpath(out_dir, chromium_root_dir)
      subprocess.check_call([executable, 'gen', '--ide=vs2017', out_dir_relative_path],
                            cwd=chromium_root_dir, env=env)

如果使用预先下载的git cache目录，配置环境变量

    set LIBCHROMIUMCONTENT_GIT_CACHE=C:\libchromiumcontent_git_cache

重新执行脚本开始编译，待完毕后执行

    python script\bootstrap.py -v --target_arch=ia32 --msvs --build_debug_libcc

生成针对 *electron* 的 *Visual Studio* 工程文件

最后执行

    python script\build.py -c D

进行编译

## 跳过 *libchromiumcontent* 拷贝发行过程，直接编译

接受 [update_dist_path.diff](https://github.com/codemeow5/chromium_lab/blob/master/update_dist_path.diff) 和 [update_dist_path_lib.diff](https://github.com/codemeow5/chromium_lab/blob/master/update_dist_path_lib.diff)补丁

从 `//vendor/libchromiumcontent/dist/main/shared_library` 拷贝 `locales` 目录到 `//vendor/libchromiumcontent/src/out-ia32/shared_library` 目录下

运行

    python script\bootstrap.py -v --target_arch=ia32 --libcc_source_path=C:\electron\vendor\libchromiumcontent\src --libcc_shared_library_path=C:\electron\vendor\libchromiumcontent\src\out-ia32\shared_library --libcc_static_library_path=C:\electron\vendor\libchromiumcontent\src\out-ia32\static_library

重新生成相关配置文件

重新执行编译

    python script\build.py -c D

## 更新 *electron*

对 `//vendor/libchromiumcontent/src` 目录进行的修改，请先生成补丁文件保存好，在进行 `//vendor/libchromiumcontent/script/update` 操作时，会执行`git clean -xdf`操作，防止更新被冲洗掉

由于 `//script/bootstrap.py` 使用 `git submodule update --init --recursive` 进行子仓库更新，如果你对子仓库（//vendor/libchromiumcontent）有修改，更新完成后，git会将你的子仓库重置为一个游离的 *HEAD* 状态，你需要手工进行 *merge* 或者 *rebase*  

首先使用 *depot_tools* 工具附带的 *git update-rebase* 命令更新 *electron* 主仓库并解决冲突代码。

    git update-rebase  

使用额外的 *--update_libcc* 参数启动 *bootstrap.py*

    python script\bootstrap.py -v --target_arch=ia32 --build_debug_libcc --update_libcc

这会更新 *electron* 仓库的submodule，并重新执行 *vendor\libchromiumcontent\script\bootstrap* 和 *vendor\libchromiumcontent\script\update* 脚本，更新 *libchromiumcontent* 仓库

