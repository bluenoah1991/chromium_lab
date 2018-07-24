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
      static Hobby* Create(const String& name) {
        return new Hobby(name);
      }
      ~Hobby();

      // https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/bindings/IDLExtendedAttributes.md#callwith_scriptstate_m_a
      void Say(ScriptState* state, const String& str);

    private:
      Hobby(const String& name);

      String name_;
    };

    } // namespace blink

    #endif // Hobby_h

> //src/third_party/WebKit/Source/core/frame/Hobby.cpp

    #include "core/frame/Hobby.h"

    #include "core/frame/LocalDOMWindow.h"
    #include "core/frame/FrameConsole.h"
    #include "core/inspector/ConsoleMessage.h"

    namespace blink {

    Hobby::Hobby(const String& name) {
      name_ = name;
    }

    Hobby::~Hobby() = default;

    void Hobby::Say(ScriptState* state, const String& str) {
      LocalDOMWindow* window = LocalDOMWindow::From(state);
      window->GetFrameConsole()->AddMessage(ConsoleMessage::Create(
         kJSMessageSource, kInfoMessageLevel,
         "Hello " + name_ + ", " + str + "."));
    }

    } // namespace blink

> //src/third_party/WebKit/Source/core/frame/Hobby.idl

    [
      Constructor(USVString name),
      Exposed=(Window,Worker)
    ] interface Hobby {
      [CallWith=ScriptState] void Say(DOMString str);
    };

### 为新添加的类提供配置GN


#### 向 *blink_core_sources("frame")* 中添加文件

> //src/third_party/WebKit/Source/core/frame/BUILD.gn

    "Hobby.h",
    "Hobby.cpp",

#### 向 *core_idl_files* 中添加文件

> //src/third_party/WebKit/Source/core/core_idl_files.gni

    "frame/Hobby.idl",

## 将实现封装成单独的组件（加速编译）

### 创建新的 *hobby* 模块

`mkdir src/third_party/WebKit/Source/core/hobby`  

> //src/third_party/WebKit/Source/core/hobby/HobbyImpl.h

    #ifndef HobbyImpl_h
    #define HobbyImpl_h

    #include "core/hobby/hobby_export.h"

    namespace blink {

    class HOBBY_EXPORT HobbyImpl {

    public:
      HobbyImpl();
      ~HobbyImpl();

      void Say();

    };

    } // namespace blink

    #endif // HobbyImpl_h

> //src/third_party/WebKit/Source/core/hobby/HobbyImpl.cpp

    #include "core/hobby/HobbyImpl.h"

    namespace blink {

    HobbyImpl::HobbyImpl() {
    }

    HobbyImpl::~HobbyImpl() = default;

    void HobbyImpl::Say() {
    }

    }
    
> //src/third_party/WebKit/Source/core/hobby/hobby_export.h

    #ifndef HOBBY_HOBBY_EXPORT_H_
    #define HOBBY_HOBBY_EXPORT_H_

    #if defined(COMPONENT_BUILD)
    #if defined(WIN32)

    #if defined(HOBBY_IMPLEMENTATION)
    #define HOBBY_EXPORT __declspec(dllexport)
    #else
    #define HOBBY_EXPORT __declspec(dllimport)
    #endif  // defined(HOBBY_IMPLEMENTATION)

    #else  // defined(WIN32)
    #if defined(HOBBY_IMPLEMENTATION)
    #define HOBBY_EXPORT __attribute__((visibility("default")))
    #else
    #define HOBBY_EXPORT
    #endif
    #endif

    #else  // defined(COMPONENT_BUILD)
    #define HOBBY_EXPORT
    #endif

    #endif  // HOBBY_HOBBY_EXPORT_H_

> //src/third_party/WebKit/Source/core/hobby/BUILD.gn

    component("hobby") {
      output_name = "hobby"
      sources = [
        "HobbyImpl.h",
        "HobbyImpl.cpp",
      ]
      defines = [ "HOBBY_IMPLEMENTATION" ]

      include_dirs = [
        "//third_party/WebKit/Source",
      ]
    }

### 将 *hobby* 组件添加到 *core* 组件的依赖

> //src/third_party/WebKit/Source/core/BUILD.gn

    ...
    
    component("core") {
    
    ...
    
    deps = [
      
    ...
    
    "//third_party/WebKit/Source/core/hobby", # 添加

### 修改 *Hobby* 类

> //src/third_party/WebKit/Source/core/frame/Hobby.h

    #ifndef Hobby_h
    #define Hobby_h

    #include "platform/bindings/ScriptWrappable.h"

    namespace blink {

    class ScriptState;
    class HobbyImpl;

    class CORE_EXPORT Hobby final : public ScriptWrappable {
      DEFINE_WRAPPERTYPEINFO();

    public:
      static Hobby* Create(const String& name) {
        return new Hobby(name);
      }
      ~Hobby();

      // https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/bindings/IDLExtendedAttributes.md#callwith_scriptstate_m_a
      void Say(ScriptState* state, const String& str);

    private:
      Hobby(const String& name);

      String name_;
      HobbyImpl *impl_;

    };

    } // namespace blink

    #endif // Hobby_h

> //src/third_party/WebKit/Source/core/frame/Hobby.cpp

    #include "core/frame/Hobby.h"

    #include "core/frame/LocalDOMWindow.h"
    #include "core/frame/FrameConsole.h"
    #include "core/inspector/ConsoleMessage.h"
    #include "core/hobby/HobbyImpl.h"

    namespace blink {

    Hobby::Hobby(const String& name) {
      name_ = name;
      impl_ = new HobbyImpl();
    }

    Hobby::~Hobby() = default;

    void Hobby::Say(ScriptState* state, const String& str) {
      LocalDOMWindow* window = LocalDOMWindow::From(state);
      window->GetFrameConsole()->AddMessage(ConsoleMessage::Create(
         kJSMessageSource, kInfoMessageLevel,
         "Hello " + name_ + ", " + str + "."));
      impl_->Say();
    }

    } // namespace blink

## 扩展 *Window* 事件

### 添加事件类型

> //src/third_party/WebKit/Source/core/events/event_type_names.json5

    ...
    
        "writeend",
        "writestart",
        "zoom",
        "hobby", // 添加
      ],
    }

### 添加事件监听器注册

> //src/third_party/WebKit/Source/core/dom/GlobalEventHandlers.h

    ...
    
    DEFINE_STATIC_ATTRIBUTE_EVENT_LISTENER(hobby);
    
    ...

### 触发事件

> //src/third_party/WebKit/Source/core/frame/Hobby.cpp

    #include "core/dom/events/Event.h"

    ...
    
    void Hobby::Say(ScriptState* state, const String& str) {
      LocalDOMWindow* window = LocalDOMWindow::From(state);
      window->GetFrameConsole()->AddMessage(ConsoleMessage::Create(
        kJSMessageSource, kInfoMessageLevel,
        "Hello " + name_ + ", " + str + "."));
      Event* hobby_event(Event::Create(EventTypeNames::hobby));
      window->DispatchEvent(hobby_event, window->document());
    }
    
    ...

## 事件传参

### 创建新的事件类型（派生自 *Event* ）

> //src/third_party/WebKit/Source/core/events/HobbyEvent.h

    #ifndef HobbyEvent_h
    #define HobbyEvent_h

    #include "core/dom/events/Event.h"

    namespace blink {

      class ScriptState;

      class HobbyEvent : public Event {
        DEFINE_WRAPPERTYPEINFO();

      public:
        static HobbyEvent* Create() { return new HobbyEvent; }

        static HobbyEvent* Create(ScriptState* state, 
                                  const AtomicString& event_type,
                                  const String& str);

        static HobbyEvent* Create(const AtomicString& event_type,
                                  const String& str);

        String str();
        void setStr(const String&);

        ~HobbyEvent() override;

      protected:
        HobbyEvent();

        HobbyEvent(const AtomicString& event_type, const String& str);

      private:
        String str_;

      };

    }

    #endif

> //src/third_party/WebKit/Source/core/events/HobbyEvent.cpp

    #include "core/events/HobbyEvent.h"

    namespace blink {

    HobbyEvent* HobbyEvent::Create(ScriptState* state, 
                                   const AtomicString& event_type,
                                   const String& str) {
      return new HobbyEvent(event_type, str);
    }

    HobbyEvent* HobbyEvent::Create(const AtomicString& event_type,
                                   const String& str) {
      return new HobbyEvent(event_type, str);
    }

    String HobbyEvent::str() {
      return str_;
    }

    void HobbyEvent::setStr(const String& str) {
      str_ = str;
    }

    HobbyEvent::HobbyEvent() : Event("", Bubbles::kNo, Cancelable::kNo) {

    }

    HobbyEvent::HobbyEvent(const AtomicString& event_type, 
                           const String& str) 
      : Event(event_type, Bubbles::kNo, Cancelable::kNo) {
      str_ = str;
    }

    HobbyEvent::~HobbyEvent() = default;

    }

> //src/third_party/WebKit/Source/core/events/HobbyEvent.idl

    [
      Constructor(DOMString event_type, DOMString str),
      ConstructorCallWith=ScriptState,
      Exposed=Window
    ] interface HobbyEvent : Event {
      attribute DOMString str;
    };

### 将 *HobbyEvent* 添加到GN构建中

> //src/third_party/WebKit/Source/core/events/BUILD.gn

    "HobbyEvent.cpp",
    "HobbyEvent.h",

> //src/third_party/WebKit/Source/core/core_idl_files.gni

    "events/HobbyEvent.idl",

## 添加触发事件代码

> //src/third_party/WebKit/Source/core/frame/Hobby.cpp

    ...
    
    #include "core/events/HobbyEvent.h"
    
    ...
    
      void Hobby::Say(ScriptState* state, const String& str) {
        String str_ = "Hello " + name_ + ", " + str + ".";
        LocalDOMWindow* window = LocalDOMWindow::From(state);
        window->GetFrameConsole()->AddMessage(ConsoleMessage::Create(
          kJSMessageSource, kInfoMessageLevel, str_));
        impl_->Say();
        HobbyEvent* hobby_event(HobbyEvent::Create(EventTypeNames::hobby, str_));
        window->DispatchEvent(hobby_event, window->document());
      }

## 创建自定义回调

### 添加新类型回调的`idl`文件

> //src/third_party/blink/renderer/core/frame/custom_callback_type.idl

    callback CustomCallback = void();

> //src/third_party/blink/renderer/bindings/core/v8/BUILD.gn

    generated_core_callback_function_files = [
    
      ...
    
      "$bindings_core_v8_output_dir/v8_custom_callback.cc",
      "$bindings_core_v8_output_dir/v8_custom_callback.h"
      
      ...

### 之后你便可以在其它地方使用该回调函数

> //src/third_party/blink/renderer/core/frame/hobby.idl

    ...
    
    void invokeWithCallback(CustomCallback callback);
    
    ...

> //src/third_party/blink/renderer/core/frame/hobby.h

    ...
    
    #include "third_party/blink/renderer/bindings/core/v8/v8_custom_callback.h"
    
    ...
    
    void invokeWithCallback(V8CustomCallback* callback);
    
    ...

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

