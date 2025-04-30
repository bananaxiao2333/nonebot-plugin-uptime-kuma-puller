from nonebot import require
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
from nonebot.log import logger
from string import Template

from nonebot import get_plugin_config
from .config import Config

__version__ = "0.1.5"

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_uptime_kuma_puller",
    description="This is a plugin that can generate a UptimeKuma status page summary for your Nonebot",
    type='application',
    usage="This is a plugin that can generate a UptimeKuma status page summary for your Nonebot",
    homepage=(
        "https://github.com/bananaxiao2333/nonebot-plugin-uptime-kuma-puller"
    ),
    config=Config,
    supported_adapters={None},
    extra={},
)

plugin_config = get_plugin_config(Config).ukp

query_uptime_kuma = on_command("健康", aliases={"uptime", "ukp"})

logger.info(
    f"Initializing nonebot_plugin_uptime_kuma_puller version: {__version__}"
)

def takeSecond(elem):
    return elem[1]

async def Query(proj_name):
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

        # 获取监控项名称列表pre
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

        # 查询每个监控项的情况pre
        heartbeat_list = heartbeat_content_js["heartbeatList"]
        for i in range(len(pub_list_ids)):
            pub_sbj = pub_list_ids[i]
            heartbeat_sbj = heartbeat_list[str(pub_sbj[0])][-1]
            # 显示在线状况
            if heartbeat_sbj["status"] == 1: # 在线状态
                status = f"{plugin_config.up_status}"
            elif heartbeat_sbj["status"] == 0: # 离线状态
                status = f"{plugin_config.down_status}"
            elif heartbeat_sbj["status"] == 2: # 重试中状态
                status = f"{plugin_config.pending_status}"
            elif heartbeat_sbj["status"] == 3: # 维护中状态
                status = f"{plugin_config.maintenance_status}"
            else:
                status = f"{plugin_config.unknown_status}"
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
            
        # 排序并生成监控项部分
        proj_msg = ""
        pub_list_ids.sort(key=takeSecond)
        for index, pub_sbj in enumerate(pub_list_ids):
            proj_msg += f"{pub_sbj[1]} {pub_sbj[2]}"
            if index != len(pub_list_ids) - 1:
                proj_msg += "\n"
        
        # 处理维护消息
        maintenance_list = []
        if plugin_config.show_maintenance:
            maintenance = content_js["maintenanceList"]
            if maintenance is not None:
                maintenance_msg = ""
                maintenance_msg_template = Template(plugin_config.maintenance_template)
                for index, value in enumerate(maintenance):
                    maintenance_msg_time = ""
                    maintenance_strategy_transed = value["strategy"]
                    if value["strategy"] in plugin_config.maintenance_time_template_list: # 注入维护时间区间
                        maintenance_msg_time_template = Template(plugin_config.maintenance_time_template_list[value["strategy"]])
                        maintenance_msg_time_mapping = {
                            "cron": value["cron"],
                            "duration": value["duration"],
                            "interval_day": value["intervalDay"],
                            "timezone": value["timezone"],
                            "timezone_offset": value["timezoneOffset"]
                        }
                        maintenance_msg_time = maintenance_msg_time_template.safe_substitute(maintenance_msg_time_mapping)
                    if value["strategy"] in plugin_config.maintenance_strategy_trans:
                        maintenance_strategy_transed = plugin_config.maintenance_strategy_trans[value["strategy"]]
                    maintenance_msg_mapping = { # 注入维护消息总成
                        "id": value["id"],
                        "title": value["title"],
                        "description": value["description"],
                        "strategy": maintenance_strategy_transed,
                        "maintenance_time": maintenance_msg_time
                    }
                    maintenance_msg += "\n" + maintenance_msg_template.safe_substitute(maintenance_msg_mapping)
        
        # 格式最后输出
        msg_template = Template(plugin_config.query_template)
        msg_template_mapping = {
            "title":proj_title,
            "proj_msg":proj_msg,
            "incident_msg":incident_msg,
            "maintenance_msg":maintenance_msg,
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
            result = await Query(proj_name)
            await query_uptime_kuma.finish(result)
    proj_name = await suggest(f"{plugin_config.suggest_proj_prompt}", plugin_config.proj_name_list, retry=plugin_config.retry, timeout=plugin_config.timeout)
    if proj_name is None:
        await query_uptime_kuma.finish(f"{plugin_config.no_arg_prompt}")
    result = await Query(proj_name)
    await query_uptime_kuma.finish(result)