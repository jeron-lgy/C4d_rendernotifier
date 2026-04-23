# Web Console Packaging Notes

当前推荐的交付形态：

- `C4D` 插件：`c4d_render_notifier/`
- 后台 watcher：`watcher/launch_web_console.bat`
- 浏览器控制台：本地 [http://127.0.0.1:37673/](http://127.0.0.1:37673/)

## 打包目标

建议最终交付为：

1. `C4D` 插件目录
2. `watcher` 可执行入口
3. 一份简短安装说明

## 打包前确认项

1. 通知发送：
   - 飞书
   - Server酱
2. 通知模板：
   - 渲染完成
   - 超时提醒
   - 测试消息
3. 托盘：
   - Open Console
   - Start Watcher
   - Stop Watcher
   - Test Send
   - Exit
4. 开机启动
5. 静默启动无黑框
6. 关闭旧进程后重新启动新版本

## 建议保留文件

- `web_console.py`
- `web_console.pyw`
- `launch_web_console.bat`
- `web/`
- `core/`

## 建议不作为主入口交付的文件

- `watcher_ui.pyw`
- `watcher_qt.pyw`
- `launch_watcher_ui.bat`
- `launch_watcher_qt.bat`
- `design_preview/`

## 后续如果打包成 exe

建议优先打包：

- `web_console.pyw`

因为它已经包含：

- watcher 后台
- tray
- web console
- 默认自动启动 watcher

这样最接近最终单入口产品形态。
