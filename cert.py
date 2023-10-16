import os

from dataclasses import dataclass


@dataclass
class AppleDevelopmentCertificate:
    name: str
    team: str


def get_env(key: str) -> str:
    if key not in os.environ:
        raise Exception(f"no `{key}` environment variable found")
    return os.environ[key]


def apple_dev_cert_from_env() -> AppleDevelopmentCertificate:
    return AppleDevelopmentCertificate(name=get_env("APPLE_DEVELOPMENT_CERT_NAME"),
                                       team=get_env("APPLE_DEVELOPMENT_CERT_TEAM"))
