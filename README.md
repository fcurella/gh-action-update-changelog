# gh-action-update-changelog

## Examples

```yml
name: Update Changelog
on:
  pull_request:
    types: [closed]

jobs:
  changelog:
    runs-on: ubuntu-latest
    if: github.event.pull_request.merged_at != null
    steps:
    - uses: actions/checkout@v2
      with:
        persist-credentials: false # otherwise, the token used is the GITHUB_TOKEN, instead of your personal token
        fetch-depth: 0 # otherwise, you will failed to push refs to dest repo
    - name: Update Changelog
      uses: "fcurella/gh-action-update-changelog@main"
      with:
          githubToken: ${{ secrets.GITHUB_TOKEN}}
          changelogPath: "CHANGELOG.rst"
          changelogLine : 4
          currentVersion: "v1.0.0"
          nextVersion: "v1.0.1"
```

## Variables

### Inputs

* `githubToken`
* `changelogPath`
* `changelogLine`
* `currentVersion`
* `nextVersion`
