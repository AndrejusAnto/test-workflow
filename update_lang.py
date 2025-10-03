import os
import requests
from collections import defaultdict

# Your GitHub username
USERNAME = "AndrejusAnto"

# Map multiple GitHub languages into grouped categories
LANG_MAP = {
    "Python": "Python",
    "Jupyter Notebook": "Python",  # treat notebooks as Python
    "C": "C",
}

# Resume file path
RESUME_FILE = "Resume.md"

# GitHub token (provided by Actions)
TOKEN = os.getenv("GITHUB_TOKEN")


def fetch_repos(username):
    repos_by_lang = defaultdict(list)
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    for repo in resp.json():
        lang = repo["language"]
        if lang in LANG_MAP:
            category = LANG_MAP[lang]
            repos_by_lang[category].append((repo["name"], repo["html_url"]))

    return repos_by_lang


def update_resume(repos_by_lang):
    with open(RESUME_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    current_lang = None

    for line in lines:
        stripped = line.strip()

        # Detect start of a language section
        if stripped.startswith("## ") and stripped.endswith(":"):
            lang_name = stripped[3:-1]  # strip "## " and ":"
            current_lang = lang_name if lang_name in repos_by_lang else None
            updated_lines.append(line)
            if current_lang:
                # Insert the new repo list for this language
                for name, url in repos_by_lang[current_lang]:
                    updated_lines.append(f"- [{name}]({url})({lang_name})\n")
                updated_lines.append("\n")
            continue

        # Skip old repo entries if we’re inside a language block
        if current_lang and stripped.startswith("- "):
            continue

        updated_lines.append(line)

    with open(RESUME_FILE, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)


if __name__ == "__main__":
    repos_by_lang = fetch_repos(USERNAME)
    update_resume(repos_by_lang)
