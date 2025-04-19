#from nonebot import require
#require("nonebot_plugin_apscheduler")
from nonebot.plugin import on_command
from datetime import datetime
import aiohttp
from nonebot.plugin import PluginMetadata
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText
from nonebot.adapters import Message
from nonebot.params import CommandArg


__version__ = "0.0.2"

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



query_uptime_kuma = on_command("健康", aliases={"uptime"})

query_url = "https://your.ip"
# TODO: setup via env
proj_name_list = ["orange","starcraft","fse"]

def takeSecond(elem):
    return elem[1]

async def OrangeUptimeQuery(proj_name):
    main_api = f"{query_url}/api/status-page/{proj_name}"
    heartbeat_api = f"{query_url}/api/status-page/heartbeat/{proj_name}"
    ret = ""
    msg = ""
    
    async with aiohttp.ClientSession() as session:
        async with session.get(main_api) as response:
            if response.status != 200:
                msg += f"主要接口查询失败：Http error {response.status}"
                return msg
            content_js = await response.json()

        async with session.get(heartbeat_api) as response:
            if response.status != 200:
                msg += f"心跳接口查询失败：Http error {response.status}"
                return msg
            heartbeat_content_js = await response.json()

    proj_title = content_js["config"]["title"]

    # 获取监控项名称列表
    pub_list = content_js["publicGroupList"]
    pub_list_ids = []
    for pub_group in pub_list:
        for pub_sbj in pub_group["monitorList"]:
            tag = ""
            if "tags" in pub_sbj:
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
        if heartbeat_sbj["status"] == 1:
            status = "🟢"
        else:
            status = "🔴"
        ping = f" {heartbeat_sbj['ping']}ms" if heartbeat_sbj["ping"] is not None else ""
        temp_txt = f"{status}{ping}"
        pub_list_ids[i].append(temp_txt)

    # 获取公告
    temp_txt = ""
    incident = content_js["incident"]
    if incident is not None:
        style = str(incident["style"]).upper()
        title = str(incident["title"])
        content = str(incident["content"])
        u_time = str(incident["lastUpdatedDate"])
        temp_txt = f"""————\n📣【{style}】{title}\n{content}\n🕰本通知更新于{u_time}\n————"""

    pub_list_ids.sort(key=takeSecond)
    for pub_sbj in pub_list_ids:
        ret += f"{pub_sbj[1]} {pub_sbj[2]}\n"
    ret += temp_txt

    msg += f"**{proj_title}查询结果**\n{ret}\n*******"
    return msg

@query_uptime_kuma.handle()
async def handle_function(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("proj_name", args)

@query_uptime_kuma.got("proj_name", prompt=f"请输入项目（可供查询的项目：{str(proj_name_list)}")
async def get_proj_name(proj_name: str = ArgPlainText()):
    proj_name = proj_name.lower()
    if proj_name not in proj_name_list:
        await query_uptime_kuma.reject(f"你想查询的 {proj_name} 不在列表（{str(proj_name_list)}）中，请重新输入！")
    result = await OrangeUptimeQuery(proj_name)
    await query_uptime_kuma.finish(result)