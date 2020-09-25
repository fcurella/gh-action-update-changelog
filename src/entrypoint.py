import datetime
import logging
import json
import os

from git import Actor, Repo
from jinja2 import Environment, FileSystemLoader

SRC_DIR = os.path.dirname(__file__)

REPOSITORY = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
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


def main():
    with open(EVENT_PATH, 'r') as fh:
        payload = json.load(fh)

    commit_sha = payload['pull_request']['merge_commit_sha']
    repo = Repo(GITHUB_WORKSPACE)
    commit = repo.commit(commit_sha)
    subject = commit.message.splitlines()[0]
    date = datetime.date.today()
    context = {
        "current_version": CURRENT_VERSION,
        "next_version": NEXT_VERSION,
        "date": date,
        "change": subject,
        "repository": REPOSITORY,
    }

    env = Environment(
        loader=FileSystemLoader(os.path.join(SRC_DIR, 'templates')),
    )
    template = env.get_template('changelog_entry.rst')
    snippet = template.render(**context)

    with open(CHANGELOG_PATH, "r") as fh:
        lines = fh.readlines()
    updated = lines[:CHANGELOG_LINE] + snippet.splitlines() + lines[CHANGELOG_LINE:]

    with open(CHANGELOG_PATH, "w") as fh:
        fh.writelines(updated)

    repo.index.add([CHANGELOG_PATH])

    author = Actor("changelog-bot", "changelog-bot@example.com")
    committer = Actor("github actions", "actions@github.com")

    # commit by commit message and author and committer
    repo.index.commit("my commit message", author=author, committer=committer)
    repo.remotes.origin = f"https://{GITHUB_ACTOR}:{GITHUB_TOKEN}@github.com/{REPOSITORY}.git"
    origin = repo.create_remote('origin', repo.remotes.origin.url)
    origin.push()


if __name__ == "__main__":
    main()
