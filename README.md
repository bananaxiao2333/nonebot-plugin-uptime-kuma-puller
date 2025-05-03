<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-uptime-kuma-puller

_✨ NoneBot UptimeKuma 抓取 ✨_

> 本插件正在持续开发中，如有问题请发Issue

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
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-uptime-kuma-puller"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:----:|:----:|:----:|:----:|
| upk__query_url | 是 | 无 | UptimeKuma 地址 |
| upk__proj_name_list | 是 | 无 | 需要监控的项目名称列表（需与 UptimeKuma 项目名称完全匹配） |
| upk__status_mapping | 否 | {0 : "🔴",1 : "🟢",2 : "🟡",3 : "🔵","unknow" : "❓"} | 状态标识 |
| upk__show_ping | 否 | True | 是否在结果中显示 Ping 测试结果 |
| upk__show_incident | 否 | True | 是否在结果中显示公告信息 |
| upk__error_prompt | 否 | 查询过程中发生错误，查询终止！ | 当发生致命错误时返回的提示信息（后附带错误信息） |
| upk__suggest_proj_prompt | 否 | 请选择需查项目 | 当未指定项目时，交互式选择的引导提示 |
| upk__no_arg_prompt | 否 | 由于用户未能提供有效参数，请重新触发指令 | 当参数缺失时返回的错误提示 |
| upk__incident_update_time_text | 否 | 🕰本通知更新于 | 公告信息中显示更新时间的前缀文本 |
| upk__show_incident_update_time | 否 | True | 是否在公告信息中显示最后更新时间 |
| upk__show_incident_type | 否 | True | 是否在公告信息中显示事故类型（如：信息/重要/危险） |
| upk__show_tags | 否 | True | 是否在结果中显示标签信息 |
| upk__show_maintenance | 否 | 是否显示维护信息 |
| upk__timeout | 否 | 30 | 超时时间（单位：秒） |
| upk__retry | 否 | 2 | 询问参数失败时的重试次数 |
| upk__incident_type_trans | 否 | `{"info":"信息","primary":"重要","danger":"危险"}` | 事故类型映射表，用于将英文类型关键词转换为中文描述 |
| upk__maintenance_strategy_trans | 否 | `{"single":"单一时间窗口","manual":"手动","cron":"命令调度"}` | 维护策略类型映射表，用于将英文类型关键词转换为中文描述 |
| upk__maintenance_time_template_list | 否 | `{"cron":"\n⊢${cron} 周期${duration}分钟（每${interval_day}天一次）\n⊢时区 ${timezone} ${timezone_offset}"}` | 维护策略描述模板映射表，支持变量替换 |
| upk__query_template | 否 | `***${title}***\n统计：${status_statistics_msg}\n${ping_statistics_msg}\n------${maintenance_msg}\n------\n${proj_msg}\n${incident_msg}\n******消耗时间${took_time}ms` | 查询结果模板，支持变量替换 |
| upk__maintenance_template | 否 | `⚠️🔵ID${id} ${title}（${strategy}）\n⊢${description}${maintenance_time}` | 否 | 维护消息模板 |
| upk__incident_template | 否 | `————\n📣${incident_style}${title}\n${content}${incident_update_time_ret}\n————` | 公告信息模板，支持变量替换 |
| upk__status_statistics_template | 否 | `${icon}:${number} ` | 状态统计模板，支持变量替换 |
| upk__ping_statistics_template | 否 | `最大${max}ms 最小${min}ms 平均${argv}ms` | PING统计模板，支持变量替换 |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| /健康 需查询项目 | 任何人 | 否 | 私聊&群聊 | 别名/uptime、/ukp |
### 效果图
暂无

## 🗺️Roadmap路线图
- [x] 永不收费永不分版本
- [x] 支持核心指令查询功能
- [x] 支持配置文件配置目标站点
- [ ] 上架Nonebot商店
- [ ] 用指令更改设置
- [ ] 重构优化，解耦代码
