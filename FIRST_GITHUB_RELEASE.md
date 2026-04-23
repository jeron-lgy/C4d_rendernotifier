# First GitHub Release Guide

这份说明用于把当前项目第一次发布到 GitHub。

## 1. 先安装 Git

请先在本机安装 Git for Windows：

[https://git-scm.com/download/win](https://git-scm.com/download/win)

安装完成后，重新打开终端，确保下面命令可用：

```powershell
git --version
```

## 2. 建议的 GitHub 仓库名

推荐：

- `tongzhi-render-notifier`

## 3. 在 GitHub 上创建空仓库

建议创建：

- Public 或 Private 都可以
- 不要勾选 `Add a README`
- 不要勾选 `.gitignore`
- 不要勾选 License

因为这些文件当前仓库里已经有了。

## 4. 首次本地初始化命令

在当前项目目录执行：

```powershell
cd C:\Users\xianka\Documents\codex\tongzhi
git init
git branch -M main
git add .
git commit -m "Initial release v1.0.0"
```

## 5. 绑定远程仓库

把下面的 `YOUR_NAME` 换成你的 GitHub 用户名：

```powershell
git remote add origin https://github.com/YOUR_NAME/tongzhi-render-notifier.git
git push -u origin main
```

## 6. 推荐发布方式

源码推送完成后，再去 GitHub 页面发一个 Release。

建议：

- Tag：`v1.0.0`
- Title：`v1.0.0`
- Description：可直接参考 [RELEASE_NOTES.md](C:/Users/xianka/Documents/codex/tongzhi/RELEASE_NOTES.md)

然后把这个文件上传为 Release 附件：

- [Tongzhi-Render-Notifier.zip](C:/Users/xianka/Documents/codex/tongzhi/release/Tongzhi-Render-Notifier.zip)

## 7. 为什么推荐这样发

这样可以把：

- 源码仓库
- 可直接使用的发布包

分开管理。

源码仓库保持干净，使用者又可以直接下载 zip 安装。

## 8. 当前已经准备好的内容

你当前仓库里已经准备好了：

- `.gitignore`
- `README.md`
- `CHANGELOG.md`
- `RELEASE_NOTES.md`
- `VERSION.txt`
- `GITHUB_PUBLISH.md`
- `release/Tongzhi-Render-Notifier.zip`

所以你真正还缺的只有：

1. 本机安装 Git
2. GitHub 上创建仓库
3. 首次 push

## 9. 等你装好 Git 之后

等你本机装好 Git 后，我可以继续直接帮你：

- 检查 Git 是否正常
- 初始化仓库
- 首次提交
- 检查提交内容是否干净
- 再给你最终 push 命令
