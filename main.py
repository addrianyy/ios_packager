import shutil
import sys

from tempfile import TemporaryDirectory

from cmdline import app_info_from_cmdline
from plist import write_entitlements_plist, write_info_plist
from provisioning_cache import get_provisioning_profile_cached
from utils import run_required_process, script_directory, create_directory

app = app_info_from_cmdline()
if app is None:
    sys.exit(1)

with TemporaryDirectory() as working_directory:
    print(f"working directory at `{working_directory}`")

    cache_directory = f"{script_directory()}/cache"

    create_directory(cache_directory)

    provisioning_profile = get_provisioning_profile_cached(app, working_directory,
                                                           cache_directory)

    print(f"provisioning profile at `{provisioning_profile.path}`")

    shutil.copy(provisioning_profile.path, f"{app.path}/embedded.mobileprovision")

    entitlements_path = f"{working_directory}/entitlements.entitlements"
    info_plist_path = f"{app.path}/Info.plist"

    write_entitlements_plist(entitlements_path, app)
    write_info_plist(info_plist_path, app)

    run_required_process(
        ["codesign", "--force", "--deep",
         "--entitlements", entitlements_path,
         "--sign", app.cert_name,
         app.path,
         ])

    print(f"prepared app `{app.path}`!")
