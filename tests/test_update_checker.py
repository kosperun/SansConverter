"""
Tests for update_checker.py.

No real network calls: fetch_latest_release()/check_for_update() are exercised
via a mocked urllib.request.urlopen so the suite stays fast and offline.
"""

import json
import urllib.error
from unittest import mock

import pytest

from update_checker import (
    UpdateInfo,
    check_for_update,
    fetch_latest_release,
    is_debian_family_linux,
    is_newer,
    parse_version,
    pick_asset_url,
)


def _release(tag_name="v2.0.3", assets=None, html_url="https://github.com/kosperun/SansConverter/releases/tag/v2.0.3"):
    return {
        "tag_name": tag_name,
        "html_url": html_url,
        "assets": assets if assets is not None else [],
    }


def _mock_response(payload: dict):
    """A context-manager mock standing in for urlopen()'s return value."""
    response = mock.MagicMock()
    response.read.return_value = json.dumps(payload).encode()
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


ASSETS = [
    {"name": "SansConverter.dmg", "browser_download_url": "https://example.com/SansConverter.dmg"},
    {"name": "SansConverter.exe", "browser_download_url": "https://example.com/SansConverter.exe"},
    {"name": "SansConverter.deb", "browser_download_url": "https://example.com/SansConverter.deb"},
    {"name": "SansConverter.tar.gz", "browser_download_url": "https://example.com/SansConverter.tar.gz"},
]


class TestParseVersion:
    @pytest.mark.parametrize(
        "version_string,expected",
        [
            ("v2.0.2", (2, 0, 2)),
            ("2.0.2", (2, 0, 2)),
            ("V1.0.0", (1, 0, 0)),
            ("2.0.10", (2, 0, 10)),
            ("10.20.30", (10, 20, 30)),
        ],
    )
    def test_parses_correctly(self, version_string, expected):
        assert parse_version(version_string) == expected

    def test_unparseable_raises(self):
        with pytest.raises(ValueError):
            parse_version("not-a-version")


class TestIsNewer:
    @pytest.mark.parametrize(
        "candidate,current,expected",
        [
            ("v2.0.3", "2.0.2", True),
            ("2.0.2", "v2.0.2", False),
            ("v2.0.1", "2.0.2", False),
            ("2.0.10", "2.0.9", True),  # numeric, not lexicographic, comparison
            ("2.1.0", "2.0.99", True),
        ],
    )
    def test_comparison(self, candidate, current, expected):
        assert is_newer(candidate, current) == expected


class TestPickAssetUrl:
    @pytest.mark.parametrize(
        "system_name,expected_url",
        [
            ("Darwin", "https://example.com/SansConverter.dmg"),
            ("Windows", "https://example.com/SansConverter.exe"),
        ],
    )
    def test_matches_platform_asset(self, system_name, expected_url):
        assert pick_asset_url(ASSETS, system_name) == expected_url

    def test_unknown_platform_returns_none(self):
        assert pick_asset_url(ASSETS, "SomeOtherOS") is None

    def test_missing_asset_returns_none(self):
        assert pick_asset_url([], "Darwin") is None

    def test_linux_debian_family_gets_deb(self):
        assert pick_asset_url(ASSETS, "Linux", debian_family=True) == "https://example.com/SansConverter.deb"

    def test_linux_non_debian_gets_tar_gz(self):
        assert pick_asset_url(ASSETS, "Linux", debian_family=False) == "https://example.com/SansConverter.tar.gz"

    def test_linux_probes_when_debian_family_not_given(self):
        with mock.patch("update_checker.is_debian_family_linux", return_value=True):
            assert pick_asset_url(ASSETS, "Linux") == "https://example.com/SansConverter.deb"
        with mock.patch("update_checker.is_debian_family_linux", return_value=False):
            assert pick_asset_url(ASSETS, "Linux") == "https://example.com/SansConverter.tar.gz"


class TestIsDebianFamilyLinux:
    @pytest.mark.parametrize(
        "os_release,expected",
        [
            ({"ID": "ubuntu", "ID_LIKE": "debian"}, True),
            ({"ID": "debian", "ID_LIKE": ""}, True),
            ({"ID": "linuxmint", "ID_LIKE": "ubuntu debian"}, True),
            ({"ID": "fedora", "ID_LIKE": ""}, False),
            ({"ID": "arch", "ID_LIKE": ""}, False),
            ({"ID": "opensuse-leap", "ID_LIKE": "suse opensuse"}, False),
        ],
    )
    def test_detects_debian_family(self, os_release, expected):
        with mock.patch("platform.freedesktop_os_release", return_value=os_release):
            assert is_debian_family_linux() == expected

    def test_returns_false_when_os_release_unreadable(self):
        with mock.patch("platform.freedesktop_os_release", side_effect=OSError("no os-release")):
            assert is_debian_family_linux() is False

    def test_returns_false_when_unsupported_python(self):
        with mock.patch("platform.freedesktop_os_release", side_effect=AttributeError):
            assert is_debian_family_linux() is False


class TestFetchLatestRelease:
    def test_returns_parsed_json_on_success(self):
        payload = _release()
        with mock.patch("urllib.request.urlopen", return_value=_mock_response(payload)):
            assert fetch_latest_release() == payload

    def test_returns_none_on_url_error(self):
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("no network")):
            assert fetch_latest_release() is None

    def test_returns_none_on_timeout(self):
        with mock.patch("urllib.request.urlopen", side_effect=TimeoutError("timed out")):
            assert fetch_latest_release() is None

    def test_returns_none_on_malformed_json(self):
        response = mock.MagicMock()
        response.read.return_value = b"not json"
        response.__enter__.return_value = response
        response.__exit__.return_value = False
        with mock.patch("urllib.request.urlopen", return_value=response):
            assert fetch_latest_release() is None


class TestCheckForUpdate:
    def test_returns_update_info_when_newer_release_exists(self):
        payload = _release(tag_name="v2.0.3", assets=ASSETS)
        with mock.patch("urllib.request.urlopen", return_value=_mock_response(payload)):
            with mock.patch("platform.system", return_value="Darwin"):
                result = check_for_update("2.0.2")
        assert result == UpdateInfo(version="2.0.3", download_url="https://example.com/SansConverter.dmg")

    def test_returns_none_when_current_version_is_latest(self):
        payload = _release(tag_name="v2.0.2", assets=ASSETS)
        with mock.patch("urllib.request.urlopen", return_value=_mock_response(payload)):
            assert check_for_update("2.0.2") is None

    def test_returns_none_when_current_version_is_newer(self):
        payload = _release(tag_name="v2.0.2", assets=ASSETS)
        with mock.patch("urllib.request.urlopen", return_value=_mock_response(payload)):
            assert check_for_update("2.0.3") is None

    def test_returns_none_on_network_failure(self):
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("no network")):
            assert check_for_update("2.0.2") is None

    def test_returns_none_when_tag_name_missing(self):
        payload = {"assets": ASSETS, "html_url": "https://example.com"}
        with mock.patch("urllib.request.urlopen", return_value=_mock_response(payload)):
            assert check_for_update("2.0.2") is None

    def test_returns_none_on_unparseable_tag(self):
        payload = _release(tag_name="not-a-version")
        with mock.patch("urllib.request.urlopen", return_value=_mock_response(payload)):
            assert check_for_update("2.0.2") is None

    def test_falls_back_to_html_url_when_no_matching_asset(self):
        payload = _release(tag_name="v2.0.3", assets=[], html_url="https://example.com/releases/tag/v2.0.3")
        with mock.patch("urllib.request.urlopen", return_value=_mock_response(payload)):
            with mock.patch("platform.system", return_value="Darwin"):
                result = check_for_update("2.0.2")
        assert result == UpdateInfo(version="2.0.3", download_url="https://example.com/releases/tag/v2.0.3")
