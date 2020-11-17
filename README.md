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
    - name: Update Changelog
      uses: "fcurella/gh-action-update-changelog@main"
      with:
        changelogPath: "CHANGELOG.md"
        changelogLine : 3
        currentVersion: "v1.0.0"
        nextVersion: "v1.0.1"
```

## Variables

### Inputs

* `changelogPath`
* `changelogLine`
* `currentVersion`
* `nextVersion`
* `commitMessage` - Optional, defaults to `"Update <changelogPath>"`.
