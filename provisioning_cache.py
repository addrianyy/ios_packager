import os
import shutil
from datetime import datetime

from app_information import AppInfo
from provisioning import ProvisioningProfile, provisioning_profile_for_app
from provisioning_request import request_provisioning_profile


def is_profile_too_old(profile: ProvisioningProfile):
    return (datetime.now() - profile.creation_date).days >= 1


def is_profile_cached(profile: ProvisioningProfile, cache_path: str):
    return profile.path == cache_path


def get_provisioning_profile_cached(app: AppInfo, working_directory: str,
                                    cache_directory: str) -> ProvisioningProfile:
    provisioning_cache_path = f"{cache_directory}/{app.bundle_id}.mobileprovision"

    provisioning_profile = provisioning_profile_for_app(app, provisioning_cache_path)
    if not provisioning_profile:
        print("no provisioning profile found")
    elif is_profile_too_old(provisioning_profile):
        print("provisioning profile is more than 1 day old")

        # Remove profile either from actual storage or from cache.
        os.remove(provisioning_profile.path)

        if is_profile_cached(provisioning_profile, provisioning_cache_path):
            # If it was cached profile then find real one and delete it too.
            provisioning_profile = provisioning_profile_for_app(app, None)
            if provisioning_profile is not None:
                os.remove(provisioning_profile.path)

        provisioning_profile = None

    if not provisioning_profile:
        request_provisioning_profile(app, working_directory)

        provisioning_profile = provisioning_profile_for_app(app, None)
        if not provisioning_profile:
            raise Exception(f"failed to get provisioning profile for `{app.bundle_id}`")

    if not is_profile_cached(provisioning_profile, provisioning_cache_path):
        shutil.copy(provisioning_profile.path, provisioning_cache_path)

    return provisioning_profile
