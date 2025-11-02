from dataclasses import dataclass


@dataclass
class AppleDevelopmentCertificate:
    bundle_namespace: str
    team: str
    name: str


def parse_certificate(cert: str) -> AppleDevelopmentCertificate:
    [bundle_namespace, team, name] = cert.split(";", 3)

    return AppleDevelopmentCertificate(bundle_namespace=bundle_namespace, team=team, name=name)
