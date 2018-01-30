## 调试相关

### 使用VSCode浏览文件时，提示 [Configuring includePath for better IntelliSense results](https://github.com/Microsoft/vscode-cpptools/blob/master/Documentation/Getting%20started.md#configuring-includepath-for-better-intellisense-results)  

需要为[.vscode/c_cpp_properties.json](https://github.com/Microsoft/vscode-cpptools/blob/master/Documentation/LanguageServer/c_cpp_properties.json.md)配置**includePath**。由于路径较多，[文档](https://github.com/Microsoft/vscode-cpptools/blob/master/Documentation/Getting%20started.md#1-use-compile_commandsjson-file-to-supply-includepaths-and-defines-information)推荐使用[compile_commands.json](http://clang.llvm.org/docs/JSONCompilationDatabase.html)进行配置。这是一种JSON Compilation Database标准格式。CMake和Ninja均支持生成这种文件。其中，Ninja支持[compdb](https://ninja-build.org/manual.html#_extra_tools)命令。具体格式如下：

> ninja -t compdb [RULES...]  # https://sarcasm.github.io/notes/dev/compilation-database.html#ninja

其中RULES信息可以从build.ninja和包含的subninja来确定，在Chromium中包含

- build.ninja
- toolchain.ninja
- win_clang_x64/toolchain.ninja

三个文件。使用文档中推荐的awk命令可以过滤出所有rule

> awk '/^rule \S+/ { print $2 }' build.ninja toolchain.ninja win_clang_x64/toolchain.ninja

将rule列表保存为rules.txt文件，并调用compdb命令生成compile_commands.json文件

> ninja -t compdb $(head -n 11 rules.txt) > compile_commands.json

最后将compile_commands.json文件路径配置到c_cpp_properties.json的compileCommands属性中。
