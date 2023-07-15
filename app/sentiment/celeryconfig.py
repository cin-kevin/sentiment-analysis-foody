import shared.config as cfg

broker_url = f"{cfg.redis_url}"
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Europe/Dublin"
enable_utc = True
