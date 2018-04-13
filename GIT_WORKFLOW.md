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

### 具体开发及 Rebase 操作

下载镜像仓库到本地

    ┌────┐                 
    │ A  │           master
    └───┬┘                 
        │                  
        │    ┌────┐        
        └──▶ │ A  │  add-on
             └────┘        

基于 `add-on` 分支，checkout 出新分支进行本地开发

    ┌────┐                                           
    │ A  │                                 master    
    └───┬┘                                           
        │                                            
        │    ┌────┐                                  
        └──▶ │ A  │                        add-on    
             └───┬┘                                  
                 │                                   
                 │    ┌────┐    ┌────┐               
                 └──▶ │ A  │───▶│ B  │     local-dev 
                      └────┘    └────┘               

此时如果在 `add-on` 分支上已经有二次开发的提交，请勿通过 `rebase` 直接更新 add-on 分支。本地特性开发完毕后，请 `merge` 进 add-on 分支

    ┌────┐                                           
    │ A  │                                 master    
    └───┬┘                                           
        │                                            
        │    ┌────┐    ┌────┐                        
        └──▶ │ A  │───▶│ B  │              add-on    
             └───┬┘    └────┘                        
                 │                                   
                 │    ┌────┐    ┌────┐               
                 └──▶ │ A  │───▶│ B  │     local-dev 
                      └────┘    └────┘               

此时，其它开发者需要 `rebase` 新的提交。

    ┌────┐                                                             
    │ A  │                                              master         
    └───┬┘                                                             
        │                                                              
        │    ┌────┐    ┌────┐                                          
        └──▶ │ A  │───▶│ B  │                           add-on         
             └───┬┘    └────┘                                          
                 │                                                     
                 │    ┌────┐    ┌────┐    ┌────┐                       
                 └──▶ │ A  │───▶│ B  │───▶│ C  │        other-local-dev
                      └────┘    └────┘    └────┘                       

当所有开发者的开发工作到一定阶段后（所有 local-dev 分支已与 add-on 分支同步完毕），对 add-on 分支进行 rebase 更新。请勿使用 Github 网站上的 Pull Request 进行 rebase 操作，Github 在操作中会更新 commit hash，导致 add-on 分支与 upstream 分支产生差异  

https://help.github.com/articles/about-pull-request-merges/#rebase-and-merge-your-pull-request-commits

    ┌────┐    ┌────┐                                           
    │ A  │───▶│ U  │                                 master    
    └───┬┘    └────┘                                           
        │                                                      
        │    ┌────┐    ┌────┐    ┌────┐    ┌────┐              
        └──▶ │ A  │───▶│ U  │───▶│ B‘ │───▶│ C‘ │    add-on    
             └───┬┘    └────┘    └────┘    └────┘              
                 │                                             
                 │    ┌────┐    ┌────┐    ┌────┐               
                 └──▶ │ A  │───▶│ B  │───▶│ C  │     local-dev 
                      └────┘    └────┘    └────┘               

所有人需要删除 `local-dev` 分支，并从 add-on 分支重新构建 `new-local-dev` 分支并继续进行开发

    ┌────┐    ┌────┐                                                       
    │ A  │───▶│ U  │                                          master       
    └───┬┘    └────┘                                                       
        │                                                                  
        │    ┌────┐    ┌────┐    ┌────┐    ┌────┐                          
        └──▶ │ A  │───▶│ U  │───▶│ B‘ │───▶│ C‘ │             add-on       
             └───┬┘    └────┘    └────┘    └────┘                          
                 │                                                         
                 │    ┌────┐    ┌────┐    ┌────┐    ┌────┐                 
                 └──▶ │ A  │───▶│ U  │───▶│ B‘ │───▶│ C‘ │    new-local-dev
                      └────┘    └────┘    └────┘    └────┘                 

### 未完结的工作

若开发者在上述 rebase 操作前有未完结的工作，需要使用 `git diff` 和 `git format-patch` 生成补丁并保存
