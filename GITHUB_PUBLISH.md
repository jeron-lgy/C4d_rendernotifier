# GitHub Publish Guide

这份说明用于把当前项目整理后发布到 GitHub。

## 一、当前建议公开的内容

建议公开这些源码和文档：

- `c4d_render_notifier/`
- `watcher/`
- `README.md`
- `CHANGELOG.md`
- `RELEASE_NOTES.md`
- `VERSION.txt`
- `DELIVERY_STRUCTURE.md`
- `RELEASE_CHECKLIST.md`
- `RELEASE_TEMPLATE.md`
- `.gitignore`

## 二、当前不建议直接提交到 GitHub 的内容

这些内容建议保留在本地，不要直接推到公开仓库：

- `build/`
- `dist/`
- `release/`
- `__pycache__/`

原因：

- `build/`、`dist/`、`release/` 都属于构建产物或发布包
- `__pycache__/` 是本地缓存
- 这些内容体积大、噪音多，不适合做源码仓库主内容

## 三、敏感信息注意事项

发布到 GitHub 前，请确认不要把本地配置文件一起提交：

`%APPDATA%\TongzhiRenderNotifier\tongzhi_render_notifier.json`

这份文件里可能包含：

- 飞书 webhook
- Server酱 SendKey
- 你的通知模板配置

这份配置文件默认不在当前仓库里，但发布前仍建议再确认一次。

## 四、推荐仓库结构

```text
tongzhi-render-notifier/
  c4d_render_notifier/
  watcher/
  README.md
  CHANGELOG.md
  VERSION.txt
  RELEASE_NOTES.md
  DELIVERY_STRUCTURE.md
  RELEASE_CHECKLIST.md
  RELEASE_TEMPLATE.md
  .gitignore
```

## 五、推荐发布方式

### 方案 A：源码仓库 + GitHub Releases

这是最推荐的方式：

1. GitHub 仓库里只放源码
2. 每次发版时，把 `release/Tongzhi-Render-Notifier.zip` 上传到 GitHub Releases

优点：

- 仓库干净
- 下载用户拿到的是直接可用的发布包
- 源码和发布物职责清楚

### 方案 B：源码仓库里直接带发布包

不太推荐，但也能用。

缺点：

- 仓库会越来越大
- 二进制更新不适合频繁进 git 历史

## 六、最短发布步骤

1. 在本地安装 Git
2. 初始化仓库
3. 提交源码
4. 在 GitHub 创建空仓库
5. 关联远程仓库并推送
6. 再把 `Tongzhi-Render-Notifier.zip` 作为 Release 附件上传

## 七、建议的仓库名

建议任选一个：

- `tongzhi-render-notifier`
- `c4d-render-notifier`
- `tongzhi-watcher`

其中最推荐：

- `tongzhi-render-notifier`

## 八、我当前能帮你做到什么

在当前环境里，我可以继续帮你：

- 检查仓库是否适合公开
- 整理 `.gitignore`
- 整理 README 和发布文档
- 准备发布包
- 给你生成首次提交和发布说明

但我当前不能直接替你推送到 GitHub，原因通常有两类：

- 当前环境没有可用的 `git`
- 当前环境没有你的 GitHub 登录态或令牌

如果你后面本机装好 Git，并且希望我继续，我可以再帮你把：

- 初始化仓库
- 首次提交
- 远程仓库绑定命令

都直接整理好。
