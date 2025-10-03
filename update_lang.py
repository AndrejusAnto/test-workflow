```python
import os
import requests

# Your GitHub username
USERNAME = "AndrejusAnto"

# Languages you want included
LANGUAGES = ["Python", "Jupyter Notebook", "C"]

# GitHub token (provided by Actions)
TOKEN = os.getenv("GITHUB_TOKEN")

# Resume file path
RESUME_FILE = "README.md"

def fetch_repos(username, languages):
    repos = []
    for lang in languages:
        url = f"https://api.github.com/users/{username}/repos?per_page=100"
        headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()

        for repo in resp.json():
            if repo["language"] == lang:
                repos.append((repo["name"], repo["html_url"], lang))
    return repos

def update_resume(repos):
    with open(RESUME_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start = "<!-- PROJECTS_START -->"
    end = "<!-- PROJECTS_END -->"

    new_list = "\n".join([f"- [{name}]({url}) ({lang})" for name, url, lang in repos])

    updated = content.split(start)[0] + start + "\n" + new_list + "\n" + end + content.split(end)[1]

    with open(RESUME_FILE, "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    repos = fetch_repos(USERNAME, LANGUAGES)
    update_resume(repos)
```
