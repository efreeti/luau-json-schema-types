# Maintainer release guide

This guide is for repository maintainers and is excluded from the npm package.
Consumer installation, usage, and development are documented in the README.

## One-time setup

Configure GitHub Actions in the npm package's **Settings → Trusted publishing**:

| Field | Value |
| --- | --- |
| Owner | `efreeti` |
| Repository | `luau-json-schema-types` |
| Workflow | `release.yml` |
| Environment | `release` |

Leave direct publishing and dist-tag permissions unchecked. The Action uses OIDC
for staged publication, so no npm token secret is required. The GitHub token must
be allowed to push release commits and tags. Configure the trusted publisher when
ready to release: npm expires unvalidated configurations after two days.

## Release

1. Open GitHub **Actions → Release to npm → Run workflow** on `main`.
2. Enter an unused stable `release_version` and a higher `next_version`.
3. The Action checks the package, commits/tags the release, stages its artifact,
   then commits and pushes the next development version.
4. Open npm's **Staged Packages** tab, inspect the artifact, and approve with 2FA.
   The version becomes public only after approval.

Alternatively, inspect and approve using a local login:

```sh
npm login
npm stage list @efreeti/luau-json-schema-types
npm stage view STAGE_ID
npm stage approve STAGE_ID
```

## Artifact and recovery

`npm run build` generates `build/package/` from the root manifest's `files` and
`luau.build` settings. It flattens `src/`, uses `init.luau` as the entry point,
and removes build metadata, development dependencies, and lifecycle scripts.
`npm run check:package` verifies its contents and typed runtime import.

If staging fails after tagging, inspect npm before retrying. If no staged artifact
exists, rebuild from the release tag and stage that output:

```sh
npm run check
npm run check:package
(cd build/package && npm stage publish)
```

If the artifact already exists, recover only any missing development commit.
Published versions cannot be reused; existing Git tags are not overwritten.

References: [trusted publishing](https://docs.npmjs.com/trusted-publishers/),
[staged publishing](https://docs.npmjs.com/staged-publishing/).
