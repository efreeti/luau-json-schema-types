# Publishing

## Wally (recommended)

Package: `efreeti/json-schema-types`. Wally scopes are tied to GitHub users or
organizations; domain verification and GPG signing are not part of this workflow.
The publishing identity must have access to the `efreeti` scope.

For a local release:

```sh
wally login
python3 scripts/check.py --luau .tools/luau --analyzer .tools/luau-analyze
python3 scripts/check-package.py wally
wally publish
```

Follow the authentication instructions shown by `wally login`. Inspect
`wally package --list` before publishing; the archive contains only the source,
Rojo entry point, Wally manifest, README, LICENSE and NOTICE.

### GitHub Actions

The **Release to Wally** Action works like Maven release preparation and publication.
Push this workflow to `main` before using it.

One-time setup:

1. Run `wally login` and complete GitHub authorization. Wally 0.3.2 stores the
   login token under `[tokens]` in `~/.wally/auth.toml`.
2. Create the GitHub environment **release** and add **WALLY_AUTH_TOKEN** as an
   environment secret containing that token. Do not commit the token or paste it
   into a chat.
3. The workflow requests `contents: write` for GitHub's built-in `GITHUB_TOKEN`.
   Repository rules must allow the Action to push commits to `main` and create
   release tags. If branch protection rejects those pushes, adjust the repository's
   release-bot permissions before running the workflow.

To release, open **Actions → Release to Wally → Run workflow**, select **main**,
and fill in:

- **release_version**: the version to publish, such as `1.0.0`.
- **next_version**: the version to leave on `main`, such as `1.0.1-dev.0`.

Both values are required. Release versions must be stable SemVer (`X.Y.Z`). The
next version can be stable or a prerelease, including `1.0.1-SNAPSHOT`; its numeric
version must be greater than the release. No versions are inferred automatically.

The Action:

1. Validates the versions, requires a new release tag, and checks authentication.
2. Sets the release version in both manifests and the README installation example.
3. Runs schema type checks and verifies the Wally archive using public synthetic cases.
4. Commits the release and creates an annotated `v<release_version>` tag. It pushes
   the release commit and tag together atomically.
5. Logs in to Wally and publishes that release, verifying the success message.
6. Sets both manifests to the next development version, commits and pushes it.
   The README keeps the published installation version.

The workflow is manual only; pushing tags does not trigger another publication.
GitHub's built-in token does not trigger the normal push CI workflow for these
commits, so this release workflow performs its own checks before publishing.
It publishes only to Wally, not npm. No GPG key or Central credentials are needed.

Publication and Git pushes cannot be one atomic operation. If Wally publication
fails after tagging, the release commit/tag remain and the development bump is not
performed. Inspect the logs and registry before retrying. If the version was not
published, check out the release tag and publish that exact version manually after
fixing authentication, then commit the planned development version on `main`.
If publication succeeded but the final push failed, only the next-version commit
needs recovery; do not publish the same version again. The workflow rejects an
existing release tag to prevent accidental reruns of a partially completed release.
It never force-pushes; concurrent branch changes cause a push failure.

Consumers use `wally install` and, for exported type aliases, `wally-package-types`
as described in the README. That type-forwarding step is required because Wally's
ordinary wrapper only forwards the runtime module.

## npm (optional)

`package.json` is ready to package the same raw Luau files as
`@efreeti/luau-json-schema-types`. Confirm you control the npm `efreeti` scope;
GitHub/Wally scope ownership does not create an npm scope automatically.

```sh
npm pack --dry-run
npm login
npm publish --access public
```

This is file distribution, not a JavaScript module. Node cannot execute this Luau
package. A consumer can mount `node_modules/@efreeti/luau-json-schema-types/src`
into a Rojo project and require that ModuleScript. The supplied Actions workflow
publishes only to Wally; npm publication is optional and manual.

References: [Wally CLI and manifest](https://github.com/UpliftGames/wally),
[Wally policies](https://wally.run/policies/),
[wally-package-types](https://github.com/JohnnyMorganz/wally-package-types).
