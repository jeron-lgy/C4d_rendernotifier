# Tongzhi Render Notifier

这是当前可交付的 `C4D 渲染通知工具` 版本。

项目已经收敛为两部分：

- `c4d_render_notifier/`
  - `C4D` 插件
  - 负责检测本机渲染状态并写入运行状态文件
- `watcher/`
  - 外部常驻 watcher
  - 负责读取运行状态、判断完成或超时、发送通知、提供托盘和 Web 控制台

## 推荐使用方式

当前推荐只使用这一套入口：

1. 把 [c4d_render_notifier](/C:/Users/xianka/Documents/codex/tongzhi/c4d_render_notifier) 整个目录复制到：
   `Cinema 4D/plugins/`
2. 启动 [watcher/launch_web_console.bat](/C:/Users/xianka/Documents/codex/tongzhi/watcher/launch_web_console.bat)
3. 在浏览器控制台里配置机器名称、通知通道和通知内容

当前最稳定的控制端是：

- [watcher/launch_web_console.bat](/C:/Users/xianka/Documents/codex/tongzhi/watcher/launch_web_console.bat)
- [watcher/web_console.py](/C:/Users/xianka/Documents/codex/tongzhi/watcher/web_console.py)
- [watcher/web/index.html](/C:/Users/xianka/Documents/codex/tongzhi/watcher/web/index.html)

其他入口目前保留在仓库里，但已经不再是主推荐路径：

- `launch_watcher.bat`
- `launch_watcher_ui.bat`
- `launch_watcher_qt.bat`
- `design_preview/`

## 当前功能

- `C4D` 手动渲染完成通知
- `C4D` 渲染队列完成通知
- 超时提醒
- 飞书 `Webhook`
- `Server酱`
- 通用 `Webhook`
- 托盘常驻
- 开机自启
- Web 控制台
- 通知模板配置
  - 渲染完成
  - 超时提醒
  - 测试消息
- 通知字段编排
  - 状态
  - 机器
  - 工程
  - 时间
  - 渲染模式
  - 输出路径
  - 开始时间

## 数据目录

所有共享数据都写在：

`%APPDATA%\TongzhiRenderNotifier\`

主要文件：

- `tongzhi_render_notifier.json`
  - 主配置文件
- `runtime_state.json`
  - 插件写入的实时渲染状态
- `plugin.log`
  - 插件日志
- `watcher.log`
  - watcher 日志
- `notify_history.json`
  - 通知历史

## 安装步骤

### 1. 安装 C4D 插件

复制：

- [c4d_render_notifier](/C:/Users/xianka/Documents/codex/tongzhi/c4d_render_notifier)

到：

`Cinema 4D/plugins/`

插件入口文件：

- [c4d_render_notifier.pyp](/C:/Users/xianka/Documents/codex/tongzhi/c4d_render_notifier/c4d_render_notifier.pyp)

### 2. 启动 watcher

运行：

- [watcher/launch_web_console.bat](/C:/Users/xianka/Documents/codex/tongzhi/watcher/launch_web_console.bat)

它会做这些事：

- 静默启动后台 watcher
- 启动本地 Web 控制台服务
- 自动打开浏览器
- 启动托盘图标

### 3. 配置通知

在浏览器控制台里完成：

- 机器名称
- 超时阈值
- 通知通道
- 开机启动
- 通知内容模板

## 依赖

当前 Web 控制台 / 托盘方案建议具备这些 Python 包：

- `pystray`
- `pillow`

如果你后面要做打包，建议参考：

- [watcher/requirements-web-console.txt](/C:/Users/xianka/Documents/codex/tongzhi/watcher/requirements-web-console.txt)
- [watcher/PACKAGE_NOTES.md](/C:/Users/xianka/Documents/codex/tongzhi/watcher/PACKAGE_NOTES.md)

## 当前边界

这版已经适合个人长期使用，但仍然有这些边界：

1. 渲染开始识别仍然来自 `C4D Python` 插件
2. 完成识别虽然已经比早期版本稳定很多，但仍然带有工程上的兜底推断逻辑
3. 输出文件兜底判断依赖实际渲染结果落盘

## 交付建议

如果你准备把这版交给别人用，建议交付时只保留这两部分：

1. `c4d_render_notifier/`
2. `watcher/`

并明确说明：

- 正式启动入口是 `watcher/launch_web_console.bat`
- 不建议使用旧的桌面 UI / Qt UI / 设计稿目录

## 打包准备

仓库里已经补了 watcher 的打包入口：

- [watcher/build_web_console.bat](/C:/Users/xianka/Documents/codex/tongzhi/watcher/build_web_console.bat)
- [watcher/web_console.spec](/C:/Users/xianka/Documents/codex/tongzhi/watcher/web_console.spec)
- [watcher/requirements-web-console.txt](/C:/Users/xianka/Documents/codex/tongzhi/watcher/requirements-web-console.txt)

建议最终打包目标：

- `TongzhiWatcher.exe`

它对应的是：

- [watcher/web_console.pyw](/C:/Users/xianka/Documents/codex/tongzhi/watcher/web_console.pyw)

额外说明见：

- [watcher/PACKAGE_NOTES.md](/C:/Users/xianka/Documents/codex/tongzhi/watcher/PACKAGE_NOTES.md)
- [DELIVERY_STRUCTURE.md](/C:/Users/xianka/Documents/codex/tongzhi/DELIVERY_STRUCTURE.md)

## 备注

- [c4d_render_notifier/constants.py](/C:/Users/xianka/Documents/codex/tongzhi/c4d_render_notifier/constants.py) 里的插件 ID 仍然是占位值，正式发布前建议替换
- 当前仓库里保留了一些历史试验入口，用于开发留档，不建议作为最终交付入口
