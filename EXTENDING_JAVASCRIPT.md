# **JAVASCRIPT** 扩展

## 扩展 **Window** 对象

### 创建 **HelloWorld** 类

> //src/third_party/WebKit/Source/core/frame/HelloWorld.h

    #ifndef HelloWorld_h
    #define HelloWorld_h

    #include "base/gtest_prod_util.h"
    #include "bindings/core/v8/serialization/SerializedScriptValue.h"
    #include "platform/bindings/ScriptWrappable.h"
    #include "platform/heap/Handle.h"
    #include "platform/wtf/Forward.h"

    namespace blink {

    class LocalFrame;
    class ExceptionState;
    class ScriptState;

    class CORE_EXPORT HelloWorld final : public ScriptWrappable,
                                         public DOMWindowClient {
      DEFINE_WRAPPERTYPEINFO();
      USING_GARBAGE_COLLECTED_MIXIN(HelloWorld);

    public:
      static HelloWorld* Create(LocalFrame* frame) { return new HelloWorld(frame); }
      void print(ScriptState*);

      void Trace(blink::Visitor*) override;

    private:
      explicit HelloWorld(LocalFrame*);

    };

    }

    #endif

> //src/third_party/WebKit/Source/core/frame/HelloWorld.cpp

    #include "HelloWorld.h"
    #include "core/frame/LocalFrame.h"

    namespace blink {

    HelloWorld::HelloWorld(LocalFrame* frame) : DOMWindowClient(frame) {
    }

    void HelloWorld::Trace(blink::Visitor* visitor) {
      ScriptWrappable::Trace(visitor);
      DOMWindowClient::Trace(visitor);
    }

    void HelloWorld::print(ScriptState*) {
    }

    }

> //src/third_party/WebKit/Source/core/frame/HelloWorld.idl

    [
      NoInterfaceObject
    ] interface HelloWorld {
      [CallWith=ScriptState] void print();
    };

### 为 **Window** 对象扩展 **World** 属性

#### 为 **DOMWindow** 类添加 **World** 虚方法

> //src/third_party/WebKit/Source/core/frame/DOMWindow.h

    class HelloWorld;
    
    ...

    public:

    ...

    virtual HelloWorld* world() const = 0; // 命名使用小写

#### 为 **LocalDOMWindow** 添加 **World** 实现

> //src/third_party/WebKit/Source/core/frame/LocalDOMWindow.h

    public:

    ...

    HelloWorld* world() const override;

    ...

    private:

    ...

    mutable Member<HelloWorld> helloworld_;

> //src/third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp

    #include "core/frame/HelloWorld.h"

    ...

    void LocalDOMWindow::Reset() {
      DCHECK(document());
      DCHECK(document()->IsContextDestroyed());
      FrameDestroyed();

      screen_ = nullptr;
      history_ = nullptr;
      locationbar_ = nullptr;
      menubar_ = nullptr;
      personalbar_ = nullptr;
      scrollbars_ = nullptr;
      statusbar_ = nullptr;
      toolbar_ = nullptr;
      navigator_ = nullptr;
      media_ = nullptr;
      custom_elements_ = nullptr;
      application_cache_ = nullptr;
      helloworld_ = nullptr; // 添加
    }

    ...

    void LocalDOMWindow::Trace(blink::Visitor* visitor) {
      visitor->Trace(document_);
      visitor->Trace(screen_);
      visitor->Trace(history_);
      visitor->Trace(locationbar_);
      visitor->Trace(menubar_);
      visitor->Trace(personalbar_);
      visitor->Trace(scrollbars_);
      visitor->Trace(statusbar_);
      visitor->Trace(toolbar_);
      visitor->Trace(navigator_);
      visitor->Trace(media_);
      visitor->Trace(custom_elements_);
      visitor->Trace(modulator_);
      visitor->Trace(external_);
      visitor->Trace(application_cache_);
      visitor->Trace(event_queue_);
      visitor->Trace(post_message_timers_);
      visitor->Trace(visualViewport_);
      visitor->Trace(event_listener_observers_);
      visitor->Trace(helloworld_); // 添加
      DOMWindow::Trace(visitor);
      Supplementable<LocalDOMWindow>::Trace(visitor);
    }

    ...

    HelloWorld* LocalDOMWindow::world() const {
      if (!helloworld_)
        helloworld_ = HelloWorld::Create(GetFrame());
      return helloworld_.Get();
    }

#### **RemoteDOMWindow** 类也需要添加

> //src/third_party/WebKit/Source/core/frame/RemoteDOMWindow.h

    public:

    ...

    HelloWorld* world() const override;

> //src/third_party/WebKit/Source/core/frame/RemoteDOMWindow.cpp

    HelloWorld* RemoteDOMWindow::world() const {
      NOTREACHED();
      return nullptr;
    }

#### Window.idl 中也需要添加定义

    [Replaceable] readonly attribute HelloWorld world;

### 为新添加的类提供配置GN


#### 向 *blink_core_sources("frame")* 中添加文件

> //src/third_party/WebKit/Source/core/frame/BUILD.gn

    "HelloWorld.h",
    "HelloWorld.cpp",

#### 向 *core_idl_files* 中添加文件

> //src/third_party/WebKit/Source/core/core_idl_files.gni

    "frame/HelloWorld.idl",

## 扩展自定义对象类型

### 创建 **Hobby** 类

> //src/third_party/WebKit/Source/core/frame/Hobby.h

    #ifndef Hobby_h
    #define Hobby_h

    #include "platform/bindings/ScriptWrappable.h"

    namespace blink {

    class ScriptState;

    class CORE_EXPORT Hobby final : public ScriptWrappable {
      DEFINE_WRAPPERTYPEINFO();

    public:
      static Hobby* Create(const String& str) {
        return new Hobby(str);
      }
      ~Hobby();

      // https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/bindings/IDLExtendedAttributes.md#callwith_scriptstate_m_a
      void Say(ScriptState* state);

    private:
      Hobby(const String& str);

      String str_;
    };

    } // namespace blink

    #endif // Hobby_h

> //src/third_party/WebKit/Source/core/frame/Hobby.cpp

    #include "core/frame/Hobby.h"

    #include "core/frame/LocalDOMWindow.h"
    #include "core/frame/FrameConsole.h"
    #include "core/inspector/ConsoleMessage.h"

    namespace blink {

    Hobby::Hobby(const String& str) {
      str_ = str;
    }

    Hobby::~Hobby() = default;

    void Hobby::Say(ScriptState* state) {
      LocalDOMWindow* window = LocalDOMWindow::From(state);
      window->GetFrameConsole()->AddMessage(ConsoleMessage::Create(
         kJSMessageSource, kInfoMessageLevel,
        str_));
    }

    } // namespace blink

> //src/third_party/WebKit/Source/core/frame/Hobby.idl

    [
      Constructor(USVString str),
      Exposed=(Window,Worker)
    ] interface Hobby {
      [CallWith=ScriptState] void Say();
    };

### 为新添加的类提供配置GN


#### 向 *blink_core_sources("frame")* 中添加文件

> //src/third_party/WebKit/Source/core/frame/BUILD.gn

    "Hobby.h",
    "Hobby.cpp",

#### 向 *core_idl_files* 中添加文件

> //src/third_party/WebKit/Source/core/core_idl_files.gni

    "frame/Hobby.idl",

## 调试

在

> //src/sandbox/win/src/target_process.cc

    ResultCode TargetProcess::Create(
    
    ...
    
    if (!::CreateProcessAsUserW(lockdown_token_.Get(), exe_path, cmd_line.get(),
    
处获取Renderer进程ID，并当

> //src/services/service_manager/sandbox/win/sandbox_win.cc

    sandbox::ResultCode SandboxWin::StartSandboxedProcess(
    
    ...
    
    CHECK(ResumeThread(target.thread_handle()) != static_cast<DWORD>(-1));
    
运行之后，Attach进程

