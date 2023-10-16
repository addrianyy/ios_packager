import plistlib

from app_information import AppInfo


def read_plist(path: str):
    with open(path, "rb") as f:
        return plistlib.load(f)


def write_plist(path: str, data):
    with open(path, "wb") as f:
        f.write(plistlib.dumps(data))


def write_info_plist(path: str, app: AppInfo):
    write_plist(path, {
        "CFBundleDevelopmentRegion": "English",
        "CFBundleExecutable": app.executable_name,
        "CFBundleGetInfoString": "",
        "CFBundleIconFile": "",
        "CFBundleIdentifier": app.bundle_id,
        "CFBundleInfoDictionaryVersion": "6.0",
        "CFBundleLongVersionString": "",
        "CFBundleName": app.bundle_name,
        "CFBundlePackageType": "APPL",
        "CFBundleShortVersionString": "",
        "CFBundleSignature": "",
        "CFBundleVersion": "",
        "CSResourcesFileMapped": "NSHumanReadableCopyright",
        "UILaunchStoryboardName": "LaunchScreen",
        "UIApplicationSupportsIndirectInputEvents": True,
    })


def write_entitlements_plist(path: str, app: AppInfo):
    write_plist(path, {
        "application-identifier": f"{app.cert_team}.{app.bundle_id}",
        "get-task-allow": True,
    })
