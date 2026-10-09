# npm setup and publication

The npm package is `@efreeti/luau-json-schema-types`. Confirm you control the npm
`efreeti` scope; GitHub/Wally ownership does not establish npm ownership.
The old Wally release remains available, but new development and releases use npm.
No npm publication has been performed by this migration.

## Dependency setup

Both libraries pin `efreeti/npmluau` to commit
`6f8c35d86ed4dd0e22cd76b4d515bc19aa8f1164`. The fork fixes Luau CLI module paths
and exported generic defaults. Installing it from Git builds its WebAssembly
module, so Node.js 24 and a compatible Rust toolchain are needed:

```sh
rustup toolchain install 1.94.0 --profile minimal --target wasm32-unknown-unknown
RUSTUP_TOOLCHAIN=1.94.0 npm ci
```

A consuming project's configuration can use:

```json
{
  "devDependencies": {
    "npmluau": "git+https://github.com/efreeti/npmluau.git#6f8c35d86ed4dd0e22cd76b4d515bc19aa8f1164"
  },
  "scripts": {
    "prepare": "npmluau --keep-luaurc --keep-rojo-configs"
  }
}
```

And `.luaurc`:

```json
{
  "aliases": { "pkg": "./node_modules/.luau-aliases" }
}
```

Imports use `require("@pkg/@efreeti/luau-json-schema-types")`. Dependencies contain
real installed files; no custom copied CLI workspace or library sourcemap is
needed. Generated links forward exported types. Conflicting nested dependency
versions are not independently resolved by the tool's shared aliases.
These are Luau packages, not JavaScript modules or TypeScript declarations.

## Build and inspect

```sh
npm run build
npm run check:package
(cd build/package && npm pack --dry-run)
```

Root `package.json` maintains metadata, `files`, and custom `luau.build` source /
output settings. npm performs file selection; the builder flattens selected `src`
files and rejects collisions. `build/package/` contains only `init.luau`,
`types.luau`, `package.json`, `README.md`, `LICENSE`, and `NOTICE`.
Generated metadata uses `main = init.luau` and removes build settings, scripts,
and development dependencies. Archives and smoke tests remain outside it.
No `default.project.json` is needed: a root init file is the module boundary.
For a Roblox game, use darklua and the game's Rojo configuration to convert
source imports into the desired instance layout. npm itself does not rewrite
imports or configure Roblox services.

## Release

The manual **Release to npm** GitHub Action takes `release_version` and
`next_version`, as the previous release workflow did. It sets and verifies the
release version, builds the artifact, commits and pushes the release/tag, publishes
`build/package/`, then commits and pushes the next development version.

Before using it:

1. Push this migration in both repositories.
2. Establish access to the npm `efreeti` scope.
3. In the GitHub environment `release`, add `NPM_TOKEN`: an npm granular token
   with permission to publish this package and bypass 2FA for automated publication.
   See [npm CI authentication](https://docs.npmjs.com/private-modules/ci-server-config/).
4. Allow the workflow's GitHub token to push release commits and tags.

Local publication after checking a stable version:

```sh
npm login
npm run check
npm run check:package
(cd build/package && npm publish --access public)
```

An already published npm version cannot be replaced. Existing Git tags also
remain; choose a new release version/tag. Publishing and Git pushes are not
atomic: if publishing fails after tagging, inspect npm before retrying. If the
version is absent, rebuild from the release tag and publish that directory. If it
is present, recover only the next development commit.
The workflow publishes nothing until manually invoked with credentials.
