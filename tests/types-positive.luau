--!strict
local Schema = require("../src")
local text: Schema.TextJSONSchema = { type = "string", format = "email", default = "a@example.test" }
local numeric: Schema.NumericJSONSchema = { type = "integer", minimum = 0, default = 1 }
local bool: Schema.BooleanJSONSchema = { type = "boolean", const = false }
local null: Schema.NullJSONSchema = { type = "null", default = nil }
local array: Schema.ArrayJSONSchema = { type = "array", items = text, const = { 1, 2 } }
local object: Schema.ObjectJSONSchema = { type = "object", properties = { a = array, b = numeric }, required = { "a" }, additionalProperties = false }
local combined: Schema.JSONSchema = { type = { "string", "null" }, anyOf = { text, null, false }, const = { a = { 1, 2 }, enabled = true } }
local expressiveText: Schema.ExpressiveTextJSONSchema = { type = "string", const = "hello" }
local choices: { read [number]: Schema.ExpressiveJSONSchema } = { expressiveText, bool }
local expressive: Schema.ExpressiveJSONSchema = { oneOf = choices }
local custom: Schema.TextJSONSchema<"custom"> = { type = "string", format = "custom" }
local values: Schema.JSONSchema = { enum = { "hello", 42, false, { 1, 2 }, { answer = 42 } } }
local nullable: Schema.JSONSchema = { type = { "string", "null" } }
type Extended = Schema.SchemaKeywords & { read ["x-provider"]: string }
local extended: Extended = { type = "object", ["x-provider"] = "efreeti" }
return { combined, expressive, custom, object, values, nullable, extended }
