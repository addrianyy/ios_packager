from dataclasses import dataclass


@dataclass
class AppInfo:
    path: str
    executable_name: str
    bundle_name: str
    bundle_id: str
    cert_team: str
    cert_name: str
