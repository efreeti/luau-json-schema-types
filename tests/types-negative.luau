--!strict
local Schema = require("../src")
local wrongBoolean: Schema.BooleanJSONSchema = { type = "boolean", default = "no" }
local wrongPrimitive: Schema.JSONSchema = { type = "unknown" }
local wrongItems: Schema.ArrayJSONSchema = { type = "array", items = 10 }
local wrongValue: Schema.JSONSchema = { const = function() end }
local wrongExpressive: Schema.ExpressiveJSONSchema = false
local wrongExpressiveItem: Schema.ExpressiveArrayJSONSchema = { type = "array", items = false }
return { wrongExpressive, wrongExpressiveItem, wrongBoolean, wrongPrimitive, wrongItems, wrongValue }
