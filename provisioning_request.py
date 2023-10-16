import os
import shutil

from app_information import AppInfo
from template import specialize_template_to_file
from utils import script_directory, run_required_process


def request_provisioning_profile(app: AppInfo, working_directory: str):
    # Disable CMake colors.
    os.environ['CLICOLOR'] = '0'

    print(f"requesting provisioning profile for `{app.bundle_id}`, this may take a while...")

    project_directory = f"{working_directory}/ios_project"
    os.mkdir(project_directory)

    static_directory = f"{script_directory()}/static"
    shutil.copy(f"{static_directory}/ios.toolchain.cmake", project_directory)
    shutil.copy(f"{static_directory}/main.m", project_directory)

    specialize_template_to_file("CMakeLists.txt", f"{project_directory}/CMakeLists.txt", [
        ("BUNDLE_NAME", app.bundle_name),
        ("BUNDLE_IDENTIFIER", app.bundle_id),
        ("TEAM_ID", app.cert_team),
    ])

    build_directory = f"{project_directory}/build"
    os.mkdir(build_directory)

    run_required_process(["cmake", "..", "-GXcode"], cwd=build_directory)
    run_required_process(
        ["cmake", "--build", ".", "--", "-allowProvisioningUpdates"],
        cwd=build_directory)

    print("done!")
