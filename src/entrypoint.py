import datetime
import logging
import json
import os

import chevron

from git import Actor, Repo

SRC_DIR = os.path.dirname(__file__)

REPOSITORY = os.environ["GITHUB_REPOSITORY"]
SHA = os.environ["GITHUB_SHA"]
EVENT = os.environ["GITHUB_EVENT_NAME"]
EVENT_PATH = os.environ["GITHUB_EVENT_PATH"]
GITHUB_WORKSPACE = os.environ["GITHUB_WORKSPACE"]
GITHUB_ACTOR = os.environ["GITHUB_ACTOR"]

GITHUB_TOKEN = os.environ["INPUT_GITHUBTOKEN"]
CURRENT_VERSION = os.environ["INPUT_CURRENTVERSION"]
NEXT_VERSION = os.environ["INPUT_NEXTVERSION"]
CHANGELOG_PATH = os.path.join(
    GITHUB_WORKSPACE, os.environ["INPUT_CHANGELOGPATH"]
)
CHANGELOG_LINE = int(os.environ["INPUT_CHANGELOGLINE"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def make_header(text, render, level="-"):
    result = render(text)
    return f"{result}\n{ level * len(result)}"


def main():
    with open(EVENT_PATH, 'r') as fh:
        payload = json.load(fh)

    commit_sha = payload['pull_request']['merge_commit_sha']
    username = payload['pull_request']['user']['login']
    repo = Repo(GITHUB_WORKSPACE)
    commit = repo.commit(commit_sha)
    subject = commit.message.splitlines()[0]
    date = datetime.date.today()
    context = {
        "current_version": CURRENT_VERSION,
        "next_version": NEXT_VERSION,
        "date": date,
        "change": subject,
        "username": username,
        "repository": REPOSITORY,
        "header": make_header,
    }

    with open(
        os.path.join(SRC_DIR, "templates", "changelog_entry.rst.mustache"),
        "r",
    ) as fh:
        snippet = chevron.render(template=fh, data=context)

    with open(CHANGELOG_PATH, "r") as fh:
        lines = fh.readlines()
    updated = lines[:CHANGELOG_LINE] + snippet.splitlines(keepends=True) + lines[CHANGELOG_LINE:]

    with open(CHANGELOG_PATH, "w") as fh:
        fh.writelines(updated)

    repo.index.add([CHANGELOG_PATH])

    author = Actor("changelog-bot", "changelog-bot@example.com")
    committer = Actor("github actions", "actions@github.com")

    # commit by commit message and author and committer
    repo.index.commit(f"📝 Update {{ CHANGELOG_PATH }}", author=author, committer=committer)
    repo.remotes.origin.set_url(f"https://{GITHUB_ACTOR}:{GITHUB_TOKEN}@github.com/{REPOSITORY}.git")
    repo.remotes.origin.push()


if __name__ == "__main__":
    main()
