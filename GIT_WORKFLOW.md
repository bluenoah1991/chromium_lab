# Git 工作流程

## 如何更新镜像仓库

针对纯净的镜像仓库，请参考

https://help.github.com/articles/duplicating-a-repository/#mirroring-a-repository-in-another-location

进行仓库的更新。由于 *Github* 上 托管的仓库存在 `pull refs`，可能导致 `git push --mirror` 过程中出错，请参考文档

http://christoph.ruegg.name/blog/git-howto-mirror-a-github-repository-without-pull-refs.html

对于包含二次开发分支的仓库，不适合使用 `git push --mirror` 命令进行提交，因为该命令会对比 upstream 仓库和 mirror 仓库的分支差异，并删除二次开发分支。所以请单独更新每个上游分支。

## Chromium 二次开发流程

### 代码拉取流程

为了二次开发工作，我们单独维护一个 chromium 镜像仓库。chromium 基于 depot_tools 中的 fetch 工具（内部封装 gclient）拉取全部源码树。为了切换到使用镜像仓库，需要在 `//depot_tools/fetch_configs` 中添加额外的目标类型。

### 分支管理

为 chromium 项目建立单独的二次开发分支（add-on），并定期进行 `rebase` 同步。由于对公共分支进行 `rebase` 操作，会导致领先的 `commit hash` 变化。所以在进行 `rebase` 之前确保所有 `add-on` 分支的衍生分支都已开发完毕并删除，`rebase` 之后，重新创建开发分支。

## Electron 二次开发流程

### 代码拉取流程

同样，我们维护单独的 electron 和 libchromiumcontent 镜像仓库。我们在开发分支上修改了 electron 对 libchromiumcontent 的 submodule 引用地址。

### 分支管理

我们为 electron 和 libchromiumcontent 项目建立单独的二次开发分支（add-on），使用类似 chromium 的开发方式进行分支管理和源码同步。

## Git 相关部分

### 具体 Rebase 操作

下载镜像仓库到
