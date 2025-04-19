<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-uptime-kuma-puller

_✨ NoneBot UptimeKuma 抓取 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/bananaxiao2333/nonebot-plugin-uptime-kuma-puller.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-template">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-template.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

这是一个简单插件，它可以从指定的UptimeKuma展示页面抓取消息并且发送出去。

## 📖 介绍

这个插件在触发指令时从指定UptimeKuma网站的指定状态页面抓取内容，返回各项在线情况并且写出钉选的通知

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-uptime-kuma-puller

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-uptime-kuma-puller
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-uptime-kuma-puller
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-uptime-kuma-puller
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-uptime-kuma-puller
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-uptime-kuma-puller"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| 配置项1 | 是 | 无 | 配置说明 |
| 配置项2 | 否 | 无 | 配置说明 |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 健康 | 任何人 | 否 | 私聊&群聊 | 别名uptime |
### 效果图
暂无

## 🗺️Roadmap路线图
- [x] 永不收费永不分版本
- [x] 支持核心指令查询功能
- [ ] 支持配置文件配置目标站点
- [ ] 上架Nonebot商店
- [ ] 用指令更改设置