import json
import os
import sys
import urllib.request
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "drew-codes-things")
HEADING = "## Recently updated"
SHOWN = 8
README = Path(__file__).resolve().parent.parent / "README.md"
API = f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed&type=owner"


def fetch_repos(token=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": f"{USER}-profile-readme"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(API, headers=headers), timeout=20) as response:
        return json.load(response)


MARKDOWN_SPECIALS = "\\[]<>"


def plain_description(description):
    one_line = " ".join((description or "").split()).replace("|", "/")
    return "".join("\\" + character if character in MARKDOWN_SPECIALS else character for character in one_line)


def project_lines(repos):
    chosen = [repo for repo in repos if not repo.get("fork") and not repo.get("archived") and repo["name"] != USER]
    chosen.sort(key=lambda repo: repo.get("pushed_at") or "", reverse=True)
    lines = []
    for repo in chosen[:SHOWN]:
        description = plain_description(repo.get("description"))
        language = f" `{repo['language']}`" if repo.get("language") else ""
        lines.append(f"- [{repo['name']}]({repo['html_url']}){language}" + (f" - {description}" if description else ""))
    return lines


def end_of_project_list(readme, position):
    for line in readme[position:].splitlines(keepends=True):
        is_list_item = line.startswith("- ")
        is_blank = not line.strip()
        if not (is_list_item or is_blank):
            break
        position += len(line)
    return position


def replace_section(readme, lines):
    section = HEADING + "\n\n" + "\n".join(lines) + "\n"
    if HEADING not in readme:
        return readme.rstrip("\n") + "\n\n" + section
    start = readme.index(HEADING)
    rest = readme[end_of_project_list(readme, start + len(HEADING)):]
    return readme[:start] + section + ("\n" + rest if rest else "")


def main():
    lines = project_lines(fetch_repos(os.environ.get("GITHUB_TOKEN")))
    if not lines:
        sys.exit("No public repositories found, leaving the README alone")
    current = README.read_text(encoding="utf-8")
    updated = replace_section(current, lines)
    if updated == current:
        print("Project list already up to date")
        return
    README.write_text(updated, encoding="utf-8")
    print(f"Project list updated with {len(lines)} repositories")


if __name__ == "__main__":
    main()
