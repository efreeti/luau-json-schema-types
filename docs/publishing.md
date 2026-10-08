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

1. Obtain a Wally auth token using Wally's login flow.
Wally 0.3.2 stores the login token under `[tokens]` in `~/.wally/auth.toml`.
Copy its value into the GitHub secret below; do not commit that file or paste the
token into a chat. The workflow logs in with the token before publishing.

2. Create the GitHub environment **release** and put the token in its environment
   secret **WALLY_AUTH_TOKEN**. Add environment reviewers if you want an approval step.
3. Set the same version in `wally.toml` and `package.json`, and commit/push all files.
4. Create and push a matching tag, for example:

```sh
git tag v0.1.0
git push origin v0.1.0
```

The **Publish to Wally** workflow checks the tag/version, runs the checks, verifies
the archive and then calls `wally publish`. Creating/pushing a matching tag requests
publication. No Central token, GPG key or GitHub write permission is needed.
No publication happened during repository setup.

For subsequent releases, update versions, commit and push a new tag. If a workflow
fails, check whether the version was already published before rerunning it.

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
