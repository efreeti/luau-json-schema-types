# Luau JSON Schema Types

Strict Luau type declarations for JSON Schema draft 2020-12, translated from
[ya-json-schema-types](https://github.com/nfroidure/ya-json-schema-types).
Schemas use ordinary Luau tables and values suitable for Roblox's `HttpService:JSONEncode`.
The package contains type declarations only. Requiring it returns an empty table;
its exported type aliases provide static checks when constructing schemas.

Wally package: **efreeti/json-schema-types**. Initial version: **1.0.0**.
The package has not been published yet.

## Install with Wally

Add this dependency to your game's `wally.toml` after the first release:

```toml
[dependencies]
JsonSchemaTypes = "efreeti/json-schema-types@1.0.0"
```

Run `wally install`. Mount `Packages/` in your Rojo project as usual. Wally's
wrapper modules do not automatically forward exported type aliases; after installing,
run [wally-package-types](https://github.com/JohnnyMorganz/wally-package-types):

```sh
rojo sourcemap default.project.json --output sourcemap.json
wally-package-types --sourcemap sourcemap.json Packages/
```

## Use in Roblox

```luau
--!strict
local HttpService = game:GetService("HttpService")
local Schema = require(game.ReplicatedStorage.Packages.JsonSchemaTypes)

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
Install the pinned tools (curl/unzip, and CMake on Intel Macs):

```sh
bash scripts/install-tools.sh
python3 scripts/check.py --luau .tools/luau --analyzer .tools/luau-analyze
python3 scripts/check-package.py .tools/wally
```

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

See [publishing instructions](docs/publishing.md) for Wally and optional npm distribution.
Apache-2.0 licensed; upstream MIT attribution is retained in [NOTICE](NOTICE).
