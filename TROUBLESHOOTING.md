## Troubleshooting

### error C2371: 'CLIENT_ID': redefinition; different basic types

错误信息中 "c:\program files (x86)\microsoft visual studio 14.0\vc\bin\amd64_x86/cl.exe" 显示当前使用的是Visual Studio 15。根据

> //src/build/toolchain/win/setup_toolchain.py  

    # Chromium requires the 10.0.14393.0 SDK or higher - previous versions don't
    # have all of the required declarations.
    args = [script_path, 'amd64_x86' if cpu == 'x86' else 'amd64']
    variables = _LoadEnvFromBat(args)

中描述，编译器会选择最新的 Windows Software Development Kit，当前使用的 10.0.16299.0 引发了该问题，需要配置为使用 10.0.15063.0

> //src/build/toolchain/win/setup_toolchain.py  

    # Chromium requires the 10.0.14393.0 SDK or higher - previous versions don't
    # have all of the required declarations.
    args = [script_path, 'amd64_x86' if cpu == 'x86' else 'amd64', '10.0.15063.0']
    variables = _LoadEnvFromBat(args)

https://groups.google.com/a/chromium.org/d/msg/chromium-dev/KdB7oW1EhiY/HIMD6jdeCQAJ  
https://chromium-review.googlesource.com/c/chromium/src/+/714366  
https://chromium-review.googlesource.com/c/chromium/src/+/714366/2/build/toolchain/win/setup_toolchain.py  
