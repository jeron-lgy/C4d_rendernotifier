# Release Checklist

当前这版已经可以按下面这份清单做最终发布整理。

## 发布包建议内容

1. `c4d_render_notifier/`
2. `watcher/TongzhiWatcher.exe`
3. `README.txt`

## 发布前自检

1. `TongzhiWatcher.exe` 可以静默启动
2. 托盘图标可以正常显示状态颜色
3. `Open Console` 可以打开控制台
4. `Start Watcher / Stop Watcher / Exit` 正常
5. 飞书通知正常
6. Server酱通知正常
7. `C4D` 手动渲染完成通知正常
8. 渲染队列通知正常
9. 超时提醒正常
10. Web 控制台里通知模板可保存

## 新机器部署说明

如果是同一用户环境，程序默认读取：

`%APPDATA%\TongzhiRenderNotifier\tongzhi_render_notifier.json`

因此：

- 同一台机器直接运行，可继承当前配置
- 新机器上如果希望沿用已有通道和模板，需要一并复制这份配置文件
- 如果不复制，也可以首次启动后在 Web 控制台里重新配置

## 建议的 README.txt 内容方向

1. 先安装 `c4d_render_notifier/` 到 `Cinema 4D/plugins/`
2. 再运行 `TongzhiWatcher.exe`
3. 浏览器里完成通道配置
4. 先执行一次测试发送
5. 再进行真实渲染验证
