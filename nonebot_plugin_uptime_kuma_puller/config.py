from pydantic import BaseModel
class ScopedConfig(BaseModel):
    query_url: str
    proj_name_list: list
    up_status: str = "🟢"
    down_status: str = "🔴"
    show_ping: bool = True
    show_incident: bool = True
    error_prompt: str = "查询过程中发生错误，查询终止！"
    suggest_proj_prompt: str = "请选择需查项目"
    no_arg_prompt: str = "由于用户未能提供有效参数，请重新触发指令"
    incident_update_time_text: str = "🕰本通知更新于"
    show_incident_update_time: bool = True
    show_incident_type: bool = True
    show_tags: bool = True
    timeout: int = 30
    retry: int = 2
    incident_type_trans: dict = {"info":"信息","primary":"重要","danger":"危险"}
    query_template: str = "***${title}***\n${main}\n******"
    incident_template: str = "————\n📣${incident_style}${title}\n${content}${incident_update_time_ret}\n————"

class Config(BaseModel):
    ukp: ScopedConfig