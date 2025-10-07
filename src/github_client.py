"""GitHub API client for fetching RHOAI data sources."""

import os
import re
import time
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote

import requests

from exceptions import GitHubAPIError, VersionNotFoundError


class GitHubAPIClient:
    """Client for accessing GitHub repositories via API."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({'Authorization': f'token {self.token}'})

        self.base_url = "https://api.github.com"
        self._rate_limit_remaining = 5000
        self._rate_limit_reset = 0

    def _make_request(self, url: str) -> requests.Response:
        """Make GitHub API request with rate limiting."""
        # Check rate limit
        if self._rate_limit_remaining <= 10 and time.time() < self._rate_limit_reset:
            sleep_time = self._rate_limit_reset - time.time() + 1
            time.sleep(sleep_time)

        response = self.session.get(url)

        # Update rate limit info
        self._rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 5000))
        self._rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))

        if response.status_code == 404:
            raise VersionNotFoundError(f"Resource not found: {url}")
        elif response.status_code != 200:
            raise GitHubAPIError(f"GitHub API error {response.status_code}: {response.text}")

        return response

    def get_file_content(self, repo: str, file_path: str) -> str:
        """Get file content from GitHub repository."""
        encoded_path = quote(file_path, safe='/')
        url = f"{self.base_url}/repos/{repo}/contents/{encoded_path}"

        response = self._make_request(url)
        data = response.json()

        if data.get('encoding') == 'base64':
            import base64
            return base64.b64decode(data['content']).decode('utf-8')
        else:
            return data.get('content', '')

    def list_directory(self, repo: str, dir_path: str) -> List[Dict]:
        """List files in a directory."""
        encoded_path = quote(dir_path, safe='/')
        url = f"{self.base_url}/repos/{repo}/contents/{encoded_path}"

        try:
            response = self._make_request(url)
            return response.json()
        except VersionNotFoundError:
            return []

    def get_olm_catalog(self, rhoai_version: str, ocp_version: str) -> str:
        """Fetch OLM catalog YAML content."""
        repo = "red-hat-data-services/RHOAI-Build-Config"

        # Try specific version path first
        file_path = f"catalog/rhoai-{rhoai_version}/v{ocp_version}/rhods-operator/catalog.yaml"
        try:
            return self.get_file_content(repo, file_path)
        except VersionNotFoundError:
            pass

        # Try pre-compiled catalog fallback
        file_path = f"pcc/catalog-v{ocp_version}.yaml"
        try:
            return self.get_file_content(repo, file_path)
        except VersionNotFoundError:
            raise VersionNotFoundError(
                f"No OLM catalog found for RHOAI {rhoai_version} / OCP {ocp_version}"
            )

    def get_disconnected_helper(self, rhoai_version: str) -> str:
        """Fetch disconnected helper markdown content."""
        repo = "red-hat-data-services/rhoai-disconnected-install-helper"
        file_path = f"rhoai-{rhoai_version}.md"

        try:
            return self.get_file_content(repo, file_path)
        except VersionNotFoundError:
            # Try legacy RHODS naming
            file_path = f"rhods-{rhoai_version}.md"
            return self.get_file_content(repo, file_path)

    def get_latest_versions(self) -> Tuple[str, str]:
        """Determine latest RHOAI and OCP versions available."""
        # Get latest RHOAI version from disconnected helper
        repo = "red-hat-data-services/rhoai-disconnected-install-helper"
        files = self.list_directory(repo, "")

        rhoai_versions = []
        for file_info in files:
            if file_info['type'] == 'file':
                match = re.match(r'rhoai-(\d+\.\d+)\.md', file_info['name'])
                if match:
                    rhoai_versions.append(match.group(1))

        if not rhoai_versions:
            raise VersionNotFoundError("No RHOAI versions found")

        # Sort versions and get latest
        rhoai_versions.sort(key=lambda v: [int(x) for x in v.split('.')])
        latest_rhoai = rhoai_versions[-1]

        # Get latest OCP version from build config
        build_repo = "red-hat-data-services/RHOAI-Build-Config"
        catalog_dirs = self.list_directory(build_repo, f"catalog/rhoai-{latest_rhoai}")

        ocp_versions = []
        for dir_info in catalog_dirs:
            if dir_info['type'] == 'dir':
                match = re.match(r'v(\d+\.\d+)', dir_info['name'])
                if match:
                    ocp_versions.append(match.group(1))

        if not ocp_versions:
            # Fallback to common latest version
            return latest_rhoai, "4.20"

        ocp_versions.sort(key=lambda v: [int(x) for x in v.split('.')])
        latest_ocp = ocp_versions[-1]

        return latest_rhoai, latest_ocp