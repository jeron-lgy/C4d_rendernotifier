# Release Template

后续发布新版本时，可以按这份模板快速整理发布说明。

---

# Release Notes

## vX.Y.Z

发布日期：YYYY-MM-DD

一句话说明这版的定位，例如：

这是一个以稳定性修复为主的小版本更新。

### 本版新增

- 

### 本版优化

- 

### 本版修复

- 

### 升级说明

- 是否需要替换 `C4D` 插件目录
- 是否需要替换 `TongzhiWatcher.exe`
- 是否需要迁移 `%APPDATA%\TongzhiRenderNotifier\` 配置

### 配置说明

主配置文件位置：

`%APPDATA%\TongzhiRenderNotifier\tongzhi_render_notifier.json`

### 备注

- 如果浏览器控制台页面没有更新，按一次 `Ctrl + F5`
- 如果后台仍是旧版 watcher，请先从托盘退出再启动新版
