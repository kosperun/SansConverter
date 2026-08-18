"""Checks GitHub Releases for a newer version of SansConverter."""

import json
import platform
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional

GITHUB_API_URL = "https://api.github.com/repos/kosperun/SansConverter/releases/latest"
REQUEST_TIMEOUT_SECONDS = 5

# Maps platform.system() to the release asset filename built for it.
# Linux is special-cased below: only Debian-family distros (Ubuntu, Debian,
# Mint, ...) get the .deb — anything else falls back to the generic .tar.gz,
# since the CI build only publishes those two Linux artifacts.
PLATFORM_ASSET_NAMES = {
    "Darwin": "SansConverter.dmg",
    "Windows": "SansConverter.exe",
}
LINUX_DEBIAN_FAMILY_ASSET_NAME = "SansConverter.deb"
LINUX_FALLBACK_ASSET_NAME = "SansConverter.tar.gz"


def is_debian_family_linux() -> bool:
    """True on Debian/Ubuntu/Mint/etc., based on /etc/os-release's ID/ID_LIKE fields."""
    try:
        os_release = platform.freedesktop_os_release()
    except (OSError, AttributeError):
        return False
    ids = {os_release.get("ID", "")} | set(os_release.get("ID_LIKE", "").split())
    return "debian" in ids


@dataclass
class UpdateInfo:
    version: str
    download_url: str


def parse_version(version_string: str) -> tuple:
    """Parses "v2.0.10" or "2.0.10" into (2, 0, 10) for numeric comparison."""
    stripped = version_string.lstrip("vV")
    return tuple(int(part) for part in stripped.split("."))


def is_newer(candidate: str, current: str) -> bool:
    """True if 'candidate' is a newer version than 'current' (both parseable by parse_version)."""
    return parse_version(candidate) > parse_version(current)


def _find_asset_url(assets: list, asset_name: str) -> Optional[str]:
    for asset in assets:
        if asset.get("name") == asset_name:
            return asset.get("browser_download_url")
    return None


def pick_asset_url(assets: list, system_name: str, debian_family: bool = None) -> Optional[str]:
    """
    Picks the download URL matching the given platform.system() value, if present.
    On Linux, 'debian_family' (probed via is_debian_family_linux() if not passed
    explicitly) decides between the .deb and the generic .tar.gz fallback.
    """
    if system_name == "Linux":
        if debian_family is None:
            debian_family = is_debian_family_linux()
        asset_name = LINUX_DEBIAN_FAMILY_ASSET_NAME if debian_family else LINUX_FALLBACK_ASSET_NAME
        return _find_asset_url(assets, asset_name)

    asset_name = PLATFORM_ASSET_NAMES.get(system_name)
    if asset_name is None:
        return None
    return _find_asset_url(assets, asset_name)


def fetch_latest_release() -> Optional[dict]:
    """Fetches the latest GitHub release. Returns None on any network/parse failure."""
    try:
        request = urllib.request.Request(GITHUB_API_URL, headers={"Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return json.loads(response.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None


def check_for_update(current_version: str) -> Optional[UpdateInfo]:
    """Returns UpdateInfo if a newer release exists, else None. Never raises."""
    release = fetch_latest_release()
    if release is None:
        return None

    tag_name = release.get("tag_name")
    if not tag_name:
        return None

    try:
        newer = is_newer(tag_name, current_version)
    except ValueError:
        # Unparseable tag (e.g. a non-numeric pre-release tag) — skip silently.
        return None

    if not newer:
        return None

    download_url = pick_asset_url(release.get("assets", []), platform.system())
    if download_url is None:
        download_url = release.get("html_url")

    return UpdateInfo(version=tag_name.lstrip("vV"), download_url=download_url)
