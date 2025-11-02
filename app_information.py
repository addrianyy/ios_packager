from dataclasses import dataclass

from cert import AppleDevelopmentCertificate


@dataclass
class AppInfo:
    path: str
    executable_name: str
    bundle_name: str
    bundle_id: str
    cert: AppleDevelopmentCertificate
