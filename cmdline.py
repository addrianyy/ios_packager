import os.path
import sys
from typing import Optional

from app_information import AppInfo
from cert import apple_dev_cert_from_env
from plist import read_plist


class AppInfoPlist:
    plist_path: str
    plist: Optional[dict] = None

    def __init__(self, app_directory: str):
        self.plist_path = f"{app_directory}/Info.plist"

    def __getitem__(self, key: str) -> str:
        if self.plist is None:
            if not os.path.isfile(self.plist_path):
                raise Exception(f"cannot get bundle `{key}`: Info.plist doesn't exist")
            self.plist = read_plist(self.plist_path)

        if key not in self.plist:
            raise Exception(f"cannot get bundle `{key}`: key doesn't exist")

        return self.plist[key]

    def get_optional(self, key: str) -> Optional[str]:
        if self.plist is None:
            if os.path.isfile(self.plist_path):
                self.plist = read_plist(self.plist_path)
            else:
                return None

        if key in self.plist:
            return self.plist[key]
        else:
            return None


def app_executable_name(app_directory: str, info_plist: AppInfoPlist):
    plist_executable = info_plist.get_optional("CFBundleExecutable")
    if plist_executable is not None:
        return plist_executable

    return os.path.splitext(os.path.basename(app_directory))[0]


def app_info_from_cmdline() -> Optional[AppInfo]:
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        print("usage: ios_package application.app [bundle name] [bundle id] [executable name]")
        return None

    app_directory = arguments[0]
    if not os.path.isdir(app_directory):
        print(f"application `{app_directory}` is not a directory")
        return None

    info_plist = AppInfoPlist(app_directory)

    bundle_name = arguments[1] if len(arguments) >= 2 else info_plist["CFBundleName"]
    bundle_id = arguments[2] if len(arguments) >= 3 else info_plist["CFBundleIdentifier"]
    executable_name = arguments[3] if len(arguments) >= 4 else app_executable_name(app_directory,
                                                                                   info_plist)

    print(f"- bundle name `{bundle_name}`")
    print(f"- bundle identifier `{bundle_id}`")
    print(f"- executable name `{executable_name}`")

    apple_dev_cert = apple_dev_cert_from_env()

    return AppInfo(path=app_directory, executable_name=executable_name, bundle_name=bundle_name,
                   bundle_id=bundle_id, cert_name=apple_dev_cert.name,
                   cert_team=apple_dev_cert.team)
