import os.path
import plistlib
import subprocess
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app_information import AppInfo


@dataclass
class ProvisioningProfile:
    path: str
    application_id: str
    bundle_id: str
    team_id: str
    creation_date: datetime
    expiration_date: datetime


def parse_provisioning_profile(full_path: str) -> Optional[ProvisioningProfile]:
    if not os.path.isfile(full_path):
        return None

    result = subprocess.run(["/usr/bin/security", "cms", "-D", "-i", full_path],
                            capture_output=True)
    if result.returncode != 0:
        print(f"warning: running `security cms` on `{full_path}` failed")
        return None

    doc = plistlib.loads(result.stdout)
    try:
        application_id: str = doc["Entitlements"]["application-identifier"]
        [team_id, bundle_id] = application_id.split(".", 1)

        creation_date = doc["CreationDate"]
        expiration_date = doc["ExpirationDate"]

        return ProvisioningProfile(path=full_path, application_id=application_id,
                                   team_id=team_id, bundle_id=bundle_id,
                                   creation_date=creation_date,
                                   expiration_date=expiration_date)

    except KeyError:
        print(f"warning: provisioning certificate `{full_path}` has invalid format")

        return None


def collect_provisioning_profiles() -> list[ProvisioningProfile]:
    home_directory = os.path.expanduser('~')
    provisioning_directory = f"{home_directory}/Library/MobileDevice/Provisioning Profiles"

    profiles: list[ProvisioningProfile] = []

    for file in os.listdir(provisioning_directory):
        profile = parse_provisioning_profile(f"{provisioning_directory}/{file}")
        if profile is not None:
            profiles.append(profile)

    return profiles


def is_provisioning_profile_valid_for_app(profile: ProvisioningProfile, app: AppInfo) -> bool:
    return (profile.bundle_id == app.bundle_id and profile.team_id == app.cert_team and
            profile.expiration_date > datetime.now())


def provisioning_profile_for_app(app: AppInfo, cache_path: Optional[str]) \
        -> Optional[ProvisioningProfile]:
    if cache_path is not None and os.path.isfile(cache_path):
        cached_profile = parse_provisioning_profile(cache_path)
        if cached_profile is not None and is_provisioning_profile_valid_for_app(cached_profile,
                                                                                app):
            return cached_profile

    candidates = filter(lambda p: is_provisioning_profile_valid_for_app(p, app),
                        collect_provisioning_profiles())

    # Sort candidates so the one that will be valid for the longest time will be first.
    sorted_candidates = sorted(candidates, key=lambda p: p.expiration_date, reverse=True)
    if len(sorted_candidates) == 0:
        return None

    return sorted_candidates[0]
