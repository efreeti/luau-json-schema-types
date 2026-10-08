--!strict
local Schema = require("../src")
local fixtures = require("./FixtureData")
local examples = require("./types-positive")
assert(next(Schema :: { [string]: unknown }) == nil, "The package exports types only")
local publicCases = 0
for _, fixture in fixtures do
    if string.sub(fixture.name, 1, 6) == "cases/" then publicCases += 1 end
end
assert(publicCases == 19)
for _, fixture in fixtures do
    assert(type(fixture.schema) == "table" or type(fixture.schema) == "boolean", fixture.name)
end
assert(#examples == 7)
local schema: Schema.JSONSchema = {
    type = "object",
    properties = {
        label = { type = { "string", "null" } },
        settings = { type = "object", default = { enabled = true, retries = 3 } },
        tags = { type = "array", default = { "one", "two" } },
    },
    required = { "label" },
    additionalProperties = false,
}
assert(type(schema) == "table")
local properties = schema.properties
assert(properties ~= nil)
local settings = properties.settings
assert(type(settings) == "table")
local default = settings.default :: Schema.JsonObject
assert(type(default) == "table")
assert(default["enabled"] == true)
assert(default["retries"] == 3)
assert(default["@type"] == nil)
print("PASS " .. tostring(#fixtures) .. " schema fixtures and native construction checks")
