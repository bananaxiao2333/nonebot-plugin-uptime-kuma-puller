from pydantic import BaseModel
class ScopedConfig(BaseModel):
    query_url: str
    proj_name_list: list
    status_mapping: dict = {
        0 : "🔴",
        1 : "🟢",
        2 : "🟡",
        3 : "🔵",
        "unknow" : "❓"
    }
    show_ping: bool = True
    show_incident: bool = True
    show_maintenance: bool = True
    error_prompt: str = "查询过程中发生错误，查询终止！"
    suggest_proj_prompt: str = "请选择需查项目"
    no_arg_prompt: str = "由于用户未能提供有效参数，请重新触发指令"
    incident_update_time_text: str = "🕰本通知更新于"
    show_incident_update_time: bool = True
    show_incident_type: bool = True
    show_tags: bool = True
    timeout: int = 30
    retry: int = 2
    incident_type_trans: dict = {
        "info":"信息",
        "primary":"重要",
        "danger":"危险"
    }
    maintenance_strategy_trans: dict = {
        "single":"单一时间窗口",
        "manual":"手动",
        "cron":"命令调度"
    }
    maintenance_time_template_list: dict = {
        "cron":"\n⊢${cron} 周期${duration}分钟（每${interval_day}天一次）\n⊢时区 ${timezone} ${timezone_offset}"
    }
    query_template: str = "***${title}***\n统计：${status_statistics_msg}\n${ping_statistics_msg}\n------${maintenance_msg}\n------\n${proj_msg}\n${incident_msg}\n******消耗时间${took_time}ms"
    maintenance_template: str = "⚠️🔵ID${id} ${title}（${strategy}）\n⊢${description}${maintenance_time}"
    incident_template: str = "————\n📣${incident_style}${title}\n${content}${incident_update_time_ret}\n————"
    status_statistics_template: str = "${icon}:${number} "
    ping_statistics_template: str = "最大${max}ms 最小${min}ms 平均${argv}ms"

class Config(BaseModel):
    ukp: ScopedConfig