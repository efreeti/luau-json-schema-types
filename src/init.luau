--!strict
-- Public entry point: forward schema type declarations.
local Types = require("@self/types")

export type JSONSchemaPrimitive = Types.JSONSchemaPrimitive
export type JSONSchemaFormat = Types.JSONSchemaFormat
export type JsonNull = Types.JsonNull
export type JsonArray = Types.JsonArray
export type JsonObject = Types.JsonObject
export type JSONSchemaValue = Types.JSONSchemaValue
export type JSONSchemaTypedProperties = Types.JSONSchemaTypedProperties
export type JSONSchemaPrimitiveTypes = Types.JSONSchemaPrimitiveTypes
export type FalseJSONSchema = Types.FalseJSONSchema
export type TrueJSONSchema = Types.TrueJSONSchema
export type JSONSchema = Types.JSONSchema
export type SchemaKeywords = Types.SchemaKeywords
export type BaseJSONSchema = Types.BaseJSONSchema
export type ValueOnlyJSONSchema = Types.ValueOnlyJSONSchema
export type NullJSONSchema = Types.NullJSONSchema
export type BooleanJSONSchema = Types.BooleanJSONSchema
export type NumericJSONSchema = Types.NumericJSONSchema
export type TextJSONSchema<F = JSONSchemaFormat> = Types.TextJSONSchema<F>
export type ArrayJSONSchema = Types.ArrayJSONSchema
export type ObjectJSONSchema = Types.ObjectJSONSchema
export type NestedJSONSchema = Types.NestedJSONSchema
export type ComposedJSONSchema = Types.ComposedJSONSchema
export type TypedJSONSchema = Types.TypedJSONSchema
export type ExpressiveTextJSONSchema<F = JSONSchemaFormat> = Types.ExpressiveTextJSONSchema<F>
export type ExpressiveArrayJSONSchema = Types.ExpressiveArrayJSONSchema
export type ExpressiveObjectJSONSchema = Types.ExpressiveObjectJSONSchema
export type ExpressiveJSONSchema = Types.ExpressiveJSONSchema

return table.freeze({})
