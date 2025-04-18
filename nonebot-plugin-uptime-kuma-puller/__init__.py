from nonebot import require, get_bot
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
import nonebot.permission
from nonebot.log import logger
# from opengsq.protocols import GameSpy4
#TODO: likely useless import, delete
from datetime import datetime
from nonebot.params import RawCommand
from nonebot.adapters.onebot.v11 import Bot as OneBot
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Bot,GroupRequestEvent
import json
import requests


__version__ = "0.0.1"

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_uptime_kuma_puller",
    description="This is a plugin that can generate a UptimeKuma status page summary for you Nonebot",
    type='application',
    usage="This is a plugin that can generate a UptimeKuma status page summary for you Nonebot",
    homepage=(
        "https://github.com/bananaxiao2333/nonebot-plugin-uptime-kuma-puller"
    ),
    config=None,
    supported_adapters={"~onebot.v11"},
    extra={},
)



ou_q = on_command("健康",aliases={"uptime"})

query_url = "https://uptime.ooooo.ink"
# TODO: setup via env
proj_name = "orange"

main_api = "{}/api/status-page/{}".format(query_url, proj_name)
heartbeat_api = "{}/api/status-page/heartbeat/{}".format(query_url, proj_name)

def takeSecond(elem):
    return elem[1]

def OrangeUptimeQuery():
    ret = "————OrangeUptime·健康查询————\n"
    req = requests.get(main_api)
    req_heartbeat = requests.get(heartbeat_api)
    if req.status_code != 200:
        ret += "OrangeUptime主要接口查询失败：Http error {}".format(req.status_code)
        return ret
    if req_heartbeat.status_code != 200:
        ret += "OrangeUptime心跳接口查询失败：Http error {}".format(req.status_code)
        return ret
    content_js = req.json()
    heartbeat_content_js = req_heartbeat.json()
    #print(content_js)

    # 获取监控项名称列表
    pub_list = content_js["publicGroupList"]
    pub_list_ids = []
    for pub_gourp in pub_list:
        for pub_sbj in pub_gourp["monitorList"]:
            tag = ""
            if pub_sbj["tags"] != []:
                tag = "[{}]".format(pub_sbj["tags"][0]["name"])
            pub_sbj_name = "{}{}".format(tag, pub_sbj["name"])
            pub_list_ids.append([pub_sbj["id"], pub_sbj_name])
    #print(pub_list_ids)

    # 查询每个监控项的情况
    heartbeat_list = heartbeat_content_js["heartbeatList"]
    for i in range(len(pub_list_ids)):
        pub_sbj = pub_list_ids[i]
        heartbeat_sbj = heartbeat_list[str(pub_sbj[0])][-1]
        if heartbeat_sbj["status"] == 1:
            status = "🟢"
        else:
            status = "🔴"
        if heartbeat_sbj["ping"] == None:
            ping = ""
        else:
            ping = " {}ms".format(heartbeat_sbj["ping"])
        temp_txt = "{}{}".format(status, ping)
        pub_list_ids[i].append(temp_txt)
    #print(pub_list_ids)

    # 获取公告
    temp_txt = ""
    incident = content_js["incident"]
    if incident != None:
        style = str(incident["style"]).upper()
        title = str(incident["title"])
        content = str(incident["content"])
        u_time = str(incident["lastUpdatedDate"])
        temp_txt = """————\n📣【{}】{}\n{}\n🕰本通知更新于{}\n————""".format(style, title, content, u_time)
        #print(temp_txt)
    
    pub_list_ids.sort(key=takeSecond)
    for pub_sbj in pub_list_ids:
        ret += "{} {}\n".format(pub_sbj[1], pub_sbj[2])
    ret += temp_txt
    
    ret += f"\n——{datetime.now()}——"
    return ret

@ou_q.handle()
async def handle_function():
    #await asyncio.sleep(15)
    await ou_q.finish(OrangeUptimeQuery())
