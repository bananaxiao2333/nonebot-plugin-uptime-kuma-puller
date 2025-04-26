from nonebot import require
require("nonebot_plugin_alconna")
require("nonebot_plugin_waiter")
from nonebot.plugin import on_command
from datetime import datetime
import aiohttp
from nonebot.plugin import PluginMetadata
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot_plugin_waiter import suggest
from string import Template

from nonebot import get_plugin_config
from .config import Config

__version__ = "0.0.3"

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_uptime_kuma_puller",
    description="This is a plugin that can generate a UptimeKuma status page summary for your Nonebot",
    type='application',
    usage="This is a plugin that can generate a UptimeKuma status page summary for your Nonebot",
    homepage=(
        "https://github.com/bananaxiao2333/nonebot-plugin-uptime-kuma-puller"
    ),
    config=None,
    supported_adapters={"~onebot.v11"},
    extra={},
)

plugin_config = get_plugin_config(Config).ukp

query_uptime_kuma = on_command("健康", aliases={"uptime", "ukp"})

#query_url = "https://uptime.ooooo.ink"
#proj_name_list = ["orange","starcraft","fse"]

def takeSecond(elem):
    return elem[1]

async def OrangeUptimeQuery(proj_name):
    try:
        main_api = f"{plugin_config.query_url}/api/status-page/{proj_name}"
        heartbeat_api = f"{plugin_config.query_url}/api/status-page/heartbeat/{proj_name}"
        ret = ""
        msg = ""
        
        async with aiohttp.ClientSession() as session:
            async with session.get(main_api) as response:
                if response.status != 200:
                    msg += f"Http error {response.status}"
                    return msg
                content_js = await response.json()

            async with session.get(heartbeat_api) as response:
                if response.status != 200:
                    msg += f"Http error {response.status}"
                    return msg
                heartbeat_content_js = await response.json()

        proj_title = content_js["config"]["title"]

        # 获取监控项名称列表
        pub_list = content_js["publicGroupList"]
        pub_list_ids = []
        for pub_group in pub_list:
            for pub_sbj in pub_group["monitorList"]:
                tag = ""
                if "tags" in pub_sbj and plugin_config.show_tags:
                    print(pub_sbj)
                    if pub_sbj["tags"] != []:
                        tag = f"[{pub_sbj['tags'][0]['name']}]"
                pub_sbj_name = f"{tag}{pub_sbj['name']}"
                pub_list_ids.append([pub_sbj["id"], pub_sbj_name])

        # 查询每个监控项的情况
        heartbeat_list = heartbeat_content_js["heartbeatList"]
        for i in range(len(pub_list_ids)):
            pub_sbj = pub_list_ids[i]
            heartbeat_sbj = heartbeat_list[str(pub_sbj[0])][-1]
            # 显示在线状况
            if heartbeat_sbj["status"] == 1:
                status = f"{plugin_config.up_status}"
            else:
                status = f"{plugin_config.down_status}"
            # 显示数字ping
            ping = f" {heartbeat_sbj['ping']}ms" if heartbeat_sbj["ping"] is not None and plugin_config.show_ping else ""
            temp_txt = f"{status}{ping}"
            pub_list_ids[i].append(temp_txt)

        # 获取公告
        incident_msg = ""
        if plugin_config.show_incident:
            incident = content_js["incident"]
            if incident is not None:
                style = str(incident["style"])
                title = str(incident["title"])
                content = str(incident["content"])
                # 读取更新时间（由于第一次创建不更新时会显示null所以需要下列判断）
                if incident["lastUpdatedDate"] == None:
                    u_time = str(incident["createdDate"])
                else:
                    u_time = str(incident["lastUpdatedDate"])
                # 可调配置项
                if plugin_config.show_incident_update_time:
                    incident_update_time = f"\n{plugin_config.incident_update_time_text}{u_time}"
                else:
                    incident_update_time = ""
                if style.lower() in plugin_config.incident_type_trans:
                    style = plugin_config.incident_type_trans[style]
                else:
                    style = style.upper()
                if plugin_config.show_incident_type:
                    incident_style = f"【{style}】"
                else:
                    incident_style = ""
                incident_template = Template(plugin_config.incident_template)
                incident_template_mapping = {
                    "incident_style":incident_style,
                    "title":title,
                    "content":content,
                    "incident_update_time_ret":incident_update_time,
                    "time":datetime.now()
                }
                incident_msg = incident_template.safe_substitute(incident_template_mapping)
            
        # 对监控项进行排序
        pub_list_ids.sort(key=takeSecond)
        for pub_sbj in pub_list_ids:
            ret += f"{pub_sbj[1]} {pub_sbj[2]}\n"
        # 塞入公告
        ret += incident_msg
        # 格式最后输出
        msg_template = Template(plugin_config.query_template)
        msg_template_mapping = {
            "title":proj_title,
            "main":ret,
            "time":datetime.now()
        }
        msg = msg_template.safe_substitute(msg_template_mapping)
    except Exception as e:
        msg = f"{plugin_config.error_prompt}\n{e}"
    return msg

@query_uptime_kuma.handle()
async def handle_function(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        proj_name = args.extract_plain_text().lower()
        if proj_name in plugin_config.proj_name_list:
            result = await OrangeUptimeQuery(proj_name)
            await query_uptime_kuma.finish(result)
    proj_name = await suggest(f"{plugin_config.suggest_proj_prompt}", plugin_config.proj_name_list, retry=plugin_config.retry, timeout=plugin_config.timeout)
    if proj_name is None:
        await query_uptime_kuma.finish(f"{plugin_config.no_arg_prompt}")
    result = await OrangeUptimeQuery(proj_name)
    await query_uptime_kuma.finish(result)