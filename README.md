# Luau JSON Schema Types

Strict Luau type declarations for JSON Schema draft 2020-12, translated from
[ya-json-schema-types](https://github.com/nfroidure/ya-json-schema-types).
Schemas use ordinary Luau tables and values suitable for Roblox's `HttpService:JSONEncode`.
The package contains type declarations only. Requiring it returns an empty table;
its exported type aliases provide static checks when constructing schemas.

npm package: **@efreeti/luau-json-schema-types**.

## Install with npm

After the first npm publication:

```sh
npm install @efreeti/luau-json-schema-types@1.1.0
```

For consumers using filesystem aliases, install our pinned npmluau fork, run it
following installation, and map `pkg` to `./node_modules/.luau-aliases` in `.luaurc`.
The fork automatically forwards exported types, including generic defaults.
Add the following to your project's `package.json`:

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

The Git-installed tool builds its WebAssembly generator and needs Node.js 24 and
Rust (tested with 1.94.0). Install dependencies with
`RUSTUP_TOOLCHAIN=1.94.0 npm install` after installing that toolchain.

Configure `.luaurc`:

```json
{
  "aliases": { "pkg": "./node_modules/.luau-aliases" }
}
```

The generated aliases are shared across installed packages; conflicting nested
versions are not resolved independently. These are native Luau packages, not
JavaScript modules or TypeScript declarations.

```luau
--!strict
local Schema = require("@pkg/@efreeti/luau-json-schema-types")
local schema: Schema.TextJSONSchema = { type = "string", format = "email" }
```

## Use in Roblox

These examples use source imports. A consuming game uses darklua to convert
filesystem aliases to imports matching its Rojo layout before syncing to Studio.
The library does not publish a Rojo project file.

```luau
--!strict
local HttpService = game:GetService("HttpService")
local Schema = require("@pkg/@efreeti/luau-json-schema-types")

local schema: Schema.JSONSchema = {
    type = "object",
    properties = {
        label = { type = { "string", "null" } },
        settings = {
            type = "object",
            default = { enabled = true, retries = 3 },
        },
        tags = { type = "array", default = { "one", "two" } },
    },
    required = { "label" },
    additionalProperties = false,
}

local json = HttpService:JSONEncode(schema)
```

`const`, `default`, `enum`, and `examples` accept native JSON-compatible values:
strings, numbers, booleans, arrays, and objects. No wrappers, tags, or conversion
functions are required. A schema allowing null uses `type = "null"` or a type list
such as `{ "string", "null" }`.

Extension keywords belong directly on the schema table. Use an intersection to
check their shape:

```luau
type ProviderSchema = Schema.SchemaKeywords & { read ["x-provider"]: string }
local schema: ProviderSchema = {
    type = "object",
    ["x-provider"] = "efreeti",
}
local json = HttpService:JSONEncode(schema)
```

## Types and representation limits

- All 57 upstream keywords have typed recursive mappings.
- Primitive-specific and expressive aliases provide narrower static checks.
- `JsonArray` and `JsonObject` are native table types; `JsonNull` is `nil`.
- Public types expose read-only views so narrower variants compose safely. This
  does not freeze your schema tables at runtime.
- `src/types.luau` holds the declarations; `src/init.luau` forwards the public aliases.

Luau has no TypeScript conditional types, bounded generics or nonempty tuple types:
`NestedJSONSchema`, `ComposedJSONSchema` and `TypedJSONSchema` use the complete keyword
model. `TextJSONSchema<F>` supports custom format literals. TypeScript's primitive
restriction and recursively propagated extension generics are not reproduced;
local intersections allow native extension fields.

Native Luau tables cannot store an explicit nil-valued field or preserve nil array
entries. For example, `const = nil` omits `const`; it does not express JSON Schema's
`"const": null`. Similarly, `{}` does not distinguish an empty JSON array from an
empty JSON object. These are native representation limits, not handled by this
library. See [HttpService's JSON behavior](https://create.roblox.com/docs/reference/engine/classes/HttpService#JSONEncode).
Luau numbers use double precision.

There is no JSON parser, serializer, schema document validator, or validator for
instances described by a schema. Use HttpService for JSON handling. Types check
schema construction statically; an annotation or cast on `JSONDecode`'s result
provides no runtime validation.

## Develop

Requires Python 3.11+ and Luau **0.741 or newer**, including its read-only type syntax.
Install Node.js 24 and a compatible Rust toolchain for building the pinned fork.
Rust 1.94.0 was tested; it can be installed without changing the default:

```sh
rustup toolchain install 1.94.0 --profile minimal --target wasm32-unknown-unknown
RUSTUP_TOOLCHAIN=1.94.0 npm ci
bash scripts/install-tools.sh
npm run check
npm run check:package
```

`npm ci` installs dependencies and runs npmluau. There is no Wally installation,
library sourcemap, or copied CLI source workspace. In IntelliJ use the Luau plugin's
Standard platform mode without a sourcemap. Its LuauSolverV2 flag must be enabled
on older language-server versions. If installed Luau sources are excluded from
navigation, cancel that exclusion and mark their directory as a Sources Root;
`.luaurc` resolves aliases but does not register IntelliJ source roots.

Tests statically check all 19 synthetic schemas in
`tests/fixtures/cases/`, translated into native Luau values, plus construction examples
and six deliberately invalid declarations. Boolean schemas are included. JSON null
values become `nil` in these construction fixtures; nil fields and array entries
cannot preserve the source JSON. Empty objects and arrays both become `{}`. These
cases check type compatibility, not lossless serialization.
Standalone runtime checks confirm the native table representation and empty module
exports. They do not simulate HttpService or claim Roblox JSON round-trip testing.
Private landscape schemas may be kept locally in the ignored
`tests/fixtures/landscape/` directory. Add `--include-landscape` to the check command
to include them in a local run. Public CI uses only the synthetic cases.
The check script generates `tests/FixtureData.luau` automatically before checking
the types. That generated module is ignored by Git and does not need to be committed.

Apache-2.0 licensed; upstream MIT attribution is retained in [NOTICE](NOTICE).
