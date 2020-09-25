# gh-action-update-changelog

## Examples

```yml
name: Update Changelog
on:
  pull_request:
    types: [closed]

jobs:
  bumpversion:
    runs-on: ubuntu-latest
    if: github.event.pull_request.merged == 'true'
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

* `major` - Comma-separated list of labels triggering a MAJOR version bump. Defaults to `''`.
* `minor` - Comma-separated list of labels triggering a MINOR version bump. Defaults to `''`.
* `patch` - Comma-separated list of labels triggering a PATCH version bump. Defaults to `''`.
* `defaultPart` - SemVer part to fallback to if no labels are matched. Defaults to the
  special value `'null'`.
