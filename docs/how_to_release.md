---
title: How to Release
description: Explains how to release kimcp to PyPI.
---

This guide explains the release procedure using version 0.1.0 as an example.

## Release Procedure

### 1. Update CHANGELOG

Add your changes to the `[Unreleased]` section in `CHANGELOG.md`.

### 2. Update Version and CHANGELOG

```sh
mise run version 0.1.0
mise run update-changelog 0.1.0
uv lock
```

`mise run version` only edits `pyproject.toml`; `uv lock` records the new version in `uv.lock`.

### 3. Run CI Checks

```sh
mise run ci
```

### 4. Commit, Tag, and Push

```sh
git add pyproject.toml CHANGELOG.md uv.lock
git commit -m "chore: release v0.1.0"
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin main --tags
```

## Automated Publication

Pushing a tag such as `v0.1.0` runs `.github/workflows/release-pypi.yml`, creates a GitHub Release, and publishes to PyPI through Trusted Publishing.

Trusted Publishing has been configured on PyPI since v0.2.0 (v0.1.0 was uploaded by hand) with:

- Project name: `kimcp`
- Owner: `kiarina`
- Repository: `kimcp`
- Workflow: `.github/workflows/release-pypi.yml`
- Environment: `pypi`

If the publish step fails, the GitHub Release already exists. Fix the cause (an `invalid-publisher` error means the PyPI configuration above is missing or does not match), then re-run only the failed job:

```sh
gh run rerun <run-id> --failed
```

The step uses `skip-existing`, so a re-run does not fail on files that were already uploaded.

Check the release with `https://pypi.org/pypi/kimcp/<version>/json`; the unversioned `https://pypi.org/pypi/kimcp/json` can keep returning the previous version for a while after publishing.

## Manual Publication

Manual publication uses the local PyPI API token available to `uv publish`.

```sh
mise run build
mise run publish
```
