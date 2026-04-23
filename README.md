# Tongzhi Render Notifier

一个面向 `Cinema 4D` 的渲染通知工具。

它由两部分组成：

- `c4d_render_notifier/`
  - 安装到 `C4D` 的插件
  - 负责检测渲染状态并写入运行信息
- `watcher/`
  - 独立后台 watcher
  - 负责托盘常驻、读取状态、发送通知、提供 Web 控制台

适合解决这类问题：

- `C4D` 渲染完成后没有提醒
- 多台机器渲染时，不容易区分是哪台机器完成
- 希望把渲染完成或超时提醒推送到飞书、Server酱等渠道

## 当前版本

- 版本：`v1.0.0`
- 发布日期：`2026-04-24`

发布说明见：

- [RELEASE_NOTES.md](/C:/Users/xianka/Documents/codex/tongzhi/RELEASE_NOTES.md)
- [CHANGELOG.md](/C:/Users/xianka/Documents/codex/tongzhi/CHANGELOG.md)

## 主要功能

- `C4D` 手动渲染完成通知
- `C4D` 渲染队列完成通知
- 超时提醒
- 飞书 `Webhook`
- `Server酱`
- 通用 `Webhook`
- 托盘常驻
- 开机自启
- 静默启动，无黑框
- 浏览器 Web 控制台
- 中文界面
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

## 推荐使用方式

当前推荐只使用这一套正式入口：

1. 把 `c4d_render_notifier/` 整个目录复制到：
   `Cinema 4D/plugins/`
2. 运行 `TongzhiWatcher.exe`
3. 浏览器打开控制台后，完成机器名称、通知通道和通知模板配置
4. 先执行一次测试发送，再进行真实渲染验证

## 快速开始

### 1. 安装 C4D 插件

把：

- `c4d_render_notifier/`

复制到：

`Cinema 4D/plugins/`

插件入口文件是：

- `c4d_render_notifier/c4d_render_notifier.pyp`

### 2. 启动 watcher

开发环境可运行：

- `watcher/launch_web_console.bat`

发布版可直接运行：

- `watcher/TongzhiWatcher.exe`

启动后它会：

- 静默运行后台 watcher
- 启动托盘图标
- 自动打开浏览器控制台

### 3. 配置通知

在浏览器控制台中配置：

- 机器名称
- 超时阈值
- 通知通道
- 开机启动
- 通知模板
- 通知字段顺序和内容

## 配置文件位置

程序默认读取：

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

如果要迁移到另一台电脑，请重点复制：

`%APPDATA%\TongzhiRenderNotifier\tongzhi_render_notifier.json`

## 推荐发布方式

推荐使用：

- GitHub 仓库放源码
- GitHub Releases 放可直接下载的发布包

当前建议对外发布包结构见：

- [DELIVERY_STRUCTURE.md](/C:/Users/xianka/Documents/codex/tongzhi/DELIVERY_STRUCTURE.md)
- [RELEASE_CHECKLIST.md](/C:/Users/xianka/Documents/codex/tongzhi/RELEASE_CHECKLIST.md)

## 仓库说明

源码仓库里当前推荐关注：

- `c4d_render_notifier/`
- `watcher/`
- `README.md`
- `CHANGELOG.md`
- `RELEASE_NOTES.md`

这些目录或文件主要用于开发和发布过程，不建议作为最终用户入口：

- `design_preview/`
- `build/`
- `dist/`
- `release/`

## 已知边界

1. 渲染状态采集仍依赖 `C4D Python` 插件
2. 完成识别虽然已经较稳定，但仍包含兜底推断逻辑
3. 输出文件判断依赖实际渲染结果落盘

## 开发与打包

如果你要继续开发或重新打包，可参考：

- [watcher/PACKAGE_NOTES.md](/C:/Users/xianka/Documents/codex/tongzhi/watcher/PACKAGE_NOTES.md)
- [watcher/build_web_console.bat](/C:/Users/xianka/Documents/codex/tongzhi/watcher/build_web_console.bat)
- [watcher/web_console.spec](/C:/Users/xianka/Documents/codex/tongzhi/watcher/web_console.spec)

## GitHub 发布参考

如果你准备把这个项目发布到 GitHub，可参考：

- [GITHUB_PUBLISH.md](/C:/Users/xianka/Documents/codex/tongzhi/GITHUB_PUBLISH.md)
- [FIRST_GITHUB_RELEASE.md](/C:/Users/xianka/Documents/codex/tongzhi/FIRST_GITHUB_RELEASE.md)

## 备注

- `c4d_render_notifier/constants.py` 里的插件 ID 当前仍是占位值，正式长期发布前建议替换
- 当前仓库里保留了一些历史试验入口，用于开发留档
