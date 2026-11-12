import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from update_projects import HEADING, project_lines, replace_section

REPOS = [
    {"name": "Old", "html_url": "https://github.com/x/Old", "pushed_at": "2026-01-01", "language": "Python", "description": "old one"},
    {"name": "New", "html_url": "https://github.com/x/New", "pushed_at": "2026-11-01", "language": None, "description": None},
    {"name": "Forked", "html_url": "u", "pushed_at": "2026-11-02", "fork": True},
    {"name": "Gone", "html_url": "u", "pushed_at": "2026-11-02", "archived": True},
    {"name": "drew-codes-things", "html_url": "u", "pushed_at": "2026-11-03"},
]


def test_newest_own_repos_come_first_without_forks_archives_or_the_profile():
    assert project_lines(REPOS) == ["- [New](https://github.com/x/New)", "- [Old](https://github.com/x/Old) `Python` - old one"]


def test_the_section_is_added_once_then_replaced_in_place():
    readme = "# hi\n\n## Stats\nstuff\n"
    first = replace_section(readme, ["- a"])
    assert first == "# hi\n\n## Stats\nstuff\n\n## Recently updated\n\n- a\n"
    assert replace_section(first, ["- b"]).count(HEADING) == 1 and "- b" in replace_section(first, ["- b"])


def test_sections_after_it_are_kept():
    readme = "# hi\n\n## Recently updated\n\n- old\n\n## Stats\nstuff\n"
    assert replace_section(readme, ["- new"]) == "# hi\n\n## Recently updated\n\n- new\n\n## Stats\nstuff\n"


def test_text_after_the_list_without_a_heading_is_kept():
    readme = "# hi\n\n## Recently updated\n\n- old\n- older\n\nThanks for reading. [Contact](mailto:x)\n"
    assert replace_section(readme, ["- new"]) == "# hi\n\n## Recently updated\n\n- new\n\nThanks for reading. [Contact](mailto:x)\n"


def test_a_top_level_heading_after_the_list_is_kept():
    readme = "# hi\n\n## Recently updated\n\n- old\n\n# Contact\nmail me\n"
    assert replace_section(readme, ["- new"]) == "# hi\n\n## Recently updated\n\n- new\n\n# Contact\nmail me\n"
