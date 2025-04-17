import requests
import os
import sys
import re
import base64
from urllib.parse import urlparse
from urllib.parse import quote

# === Configuration ===
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"  # Set your GitHub token here

# The strings we want to search for in the project files
# These are common indicators of backdoors or malicious scripts
TARGET_STRINGS = [
    "PreBuildEvent",
    "PostBuildEvent",
    "Exec",
    "Command=",
    "@echo off",
    "cscript",
    "//nologo",
    "cmd.exe",
    "-hidden",
    "ExecutionPolicy",
    "powershell.exe",
    "wscript.exe",
    ".vbs",
]

API_BASE = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def parse_github_url(url):
    parsed = urlparse(url)
    match = re.match(r'^/([^/]+)/([^/]+?)(?:\.git)?/?$', parsed.path)
    if not match:
        raise ValueError("Invalid GitHub repository URL.")
    owner, repo = match.groups()
    return quote(owner), quote(repo)

def get_repo_default_branch(owner, repo):
    url = f"{API_BASE}/repos/{owner}/{repo}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["default_branch"]

def get_repo_tree(owner, repo, branch):
    url = f"{API_BASE}/repos/{owner}/{repo}/git/trees/{quote(branch)}?recursive=1"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["tree"]

def get_file_content(owner, repo, path):
    url = f"{API_BASE}/repos/{owner}/{repo}/contents/{quote(path)}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    content = r.json().get("content", "")
    encoding = r.json().get("encoding", "base64")
    if encoding == "base64":
        return base64.b64decode(content).decode("utf-8", errors="ignore")
    return ""

def scan_repository(repo_url):
    if not GITHUB_TOKEN:
        print("Please set the GITHUB_TOKEN variable.")
        return

    try:
        owner, repo = parse_github_url(repo_url)
        branch = get_repo_default_branch(owner, repo)
        print(f"\nScanning {owner}/{repo}@{branch}...")
        tree = get_repo_tree(owner, repo, branch)
    except Exception as e:
        print(f"Error setting up repo scan: {e}")
        return

    matches_found = {}

    for item in tree:
        if item["type"] == "blob" and (item["path"].endswith(".csproj") or item["path"].endswith(".vbproj")):
            try:
                content = get_file_content(owner, repo, item["path"])
                found = [s for s in TARGET_STRINGS if s in content]
                if len(found) >= 2:
                    matches_found[item["path"]] = found
            except Exception as e:
                print(f"Error reading {item['path']}: {e}")

    for path, found in matches_found.items():
        print(f"[!] Suspicious strings found in: {path}")
        print(f"  Matched strings: {', '.join(found)}")

    if not matches_found:
        print("Found no suspicious strings in the project files.")
    print("\nScan completed.")

if __name__ == "__main__":
    print("GitHub Backdoor Scanner - Version 1.0 - Jonathan Peters (cod3nym) 2025")
    if len(sys.argv) < 2:
        print("Usage: python repo_scanner.py https://github.com/owner/repo ...")
    else:
        for arg in sys.argv[1:]:
            scan_repository(arg)