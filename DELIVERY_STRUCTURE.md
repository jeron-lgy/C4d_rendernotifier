# Delivery Structure

建议最终对外交付结构：

```text
Tongzhi-Render-Notifier/
  c4d_render_notifier/
  watcher/
    TongzhiWatcher.exe
  README.txt
```

## 交付建议

### 给使用者的最短步骤

1. 把 `c4d_render_notifier/` 复制到 `Cinema 4D/plugins/`
2. 双击 `TongzhiWatcher.exe`
3. 浏览器打开后完成通道和通知模板配置
4. 做一次测试发送

### 当前推荐的发布主入口

- `TongzhiWatcher.exe`

它对应当前仓库中的：

- [watcher/web_console.pyw](/C:/Users/xianka/Documents/codex/tongzhi/watcher/web_console.pyw)

### 当前不建议对外暴露的开发入口

- `launch_watcher.bat`
- `launch_watcher_ui.bat`
- `launch_watcher_qt.bat`
- `launch_configurator.bat`
- `design_preview/`

这些都可以保留在源码仓库里，但不建议放进最终交付压缩包。
