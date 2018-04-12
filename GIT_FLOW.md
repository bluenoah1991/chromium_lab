# Git 工作流程

## 如何更新镜像仓库

针对纯净的镜像仓库，请参考

https://help.github.com/articles/duplicating-a-repository/#mirroring-a-repository-in-another-location

进行仓库的更新。由于 *Github* 上 托管的仓库存在 `pull refs`，可能导致 `git push --mirror` 过程中出错，请参考文档

http://christoph.ruegg.name/blog/git-howto-mirror-a-github-repository-without-pull-refs.html

对于包含二次开发分支的仓库，不适合使用 `git push --mirror` 命令进行提交，因为该命令会对比 upstream 仓库和 mirror 仓库的分支差异，并删除二次开发分支。所以请单独更新每个上游分支。

