--!strict
-- Schema vocabulary translated from ya-json-schema-types; see NOTICE.

export type JSONSchemaPrimitive = "null" | "boolean" | "object" | "array" | "number" | "integer" | "string"
export type JSONSchemaFormat = "date" | "time" | "date-time" | "duration" | "email" | "idn-email"
    | "hostname" | "idn-hostname" | "ipv4" | "ipv6" | "uri" | "uri-reference" | "iri"
    | "iri-reference" | "uuid" | "uri-template" | "json-pointer" | "relative-json-pointer" | "regex"

-- Native JSON values: nil represents null, with the usual Luau table limitations.
export type JsonNull = nil
export type JsonArray = { read [number]: JSONSchemaValue }
export type JsonObject = { read [string]: JSONSchemaValue }
export type JSONSchemaValue = boolean | number | string | JsonNull | JsonArray | JsonObject
export type JSONSchemaTypedProperties = "type" | "enum" | "const" | "default" | "examples"
export type JSONSchemaPrimitiveTypes = {
    read ["null"]: JsonNull, read boolean: boolean, read number: number, read integer: number,
    read string: string, read array: JsonArray, read object: JsonObject,
}
export type FalseJSONSchema = false
export type TrueJSONSchema = true
export type JSONSchema = boolean | SchemaKeywords
export type SchemaKeywords = {
    read ["$id"]: string?,
    read ["$comment"]: string?,
    read ["$schema"]: string?,
    read ["$anchor"]: string?,
    read ["$dynamicAnchor"]: string?,
    read ["title"]: string?,
    read ["description"]: string?,
    read ["$ref"]: string?,
    read ["$dynamicRef"]: string?,
    read ["format"]: string?,
    read ["pattern"]: string?,
    read ["contentEncoding"]: string?,
    read ["contentMediaType"]: string?,
    read ["deprecated"]: boolean?,
    read ["readOnly"]: boolean?,
    read ["writeOnly"]: boolean?,
    read ["uniqueItems"]: boolean?,
    read ["multipleOf"]: number?,
    read ["maximum"]: number?,
    read ["exclusiveMaximum"]: number?,
    read ["minimum"]: number?,
    read ["exclusiveMinimum"]: number?,
    read ["maxLength"]: number?,
    read ["minLength"]: number?,
    read ["maxItems"]: number?,
    read ["minItems"]: number?,
    read ["maxContains"]: number?,
    read ["minContains"]: number?,
    read ["maxProperties"]: number?,
    read ["minProperties"]: number?,
    read ["$defs"]: { read [string]: JSONSchema }?,
    read ["properties"]: { read [string]: JSONSchema }?,
    read ["patternProperties"]: { read [string]: JSONSchema }?,
    read ["dependentSchemas"]: { read [string]: JSONSchema }?,
    read ["$vocabulary"]: { read [string]: boolean }?,
    read ["type"]: JSONSchemaPrimitive | { read [number]: JSONSchemaPrimitive }?,
    read ["enum"]: { read [number]: JSONSchemaValue }?,
    read ["examples"]: { read [number]: JSONSchemaValue }?,
    read ["const"]: JSONSchemaValue?,
    read ["default"]: JSONSchemaValue?,
    read ["contentSchema"]: JSONSchema?,
    read ["items"]: JSONSchema?,
    read ["contains"]: JSONSchema?,
    read ["unevaluatedItems"]: JSONSchema?,
    read ["additionalProperties"]: JSONSchema?,
    read ["propertyNames"]: JSONSchema?,
    read ["unevaluatedProperties"]: JSONSchema?,
    read ["not"]: JSONSchema?,
    read ["if"]: JSONSchema?,
    read ["then"]: JSONSchema?,
    read ["else"]: JSONSchema?,
    read ["prefixItems"]: { read [number]: JSONSchema }?,
    read ["anyOf"]: { read [number]: JSONSchema }?,
    read ["allOf"]: { read [number]: JSONSchema }?,
    read ["oneOf"]: { read [number]: JSONSchema }?,
    read ["required"]: { read [number]: string }?,
    read ["dependentRequired"]: { read [string]: { read [number]: string } }?,
}

export type BaseJSONSchema = {
    read ["$id"]: string?, read ["$comment"]: string?, read ["$schema"]: string?,
    read ["$vocabulary"]: { read [string]: boolean }?, read ["$anchor"]: string?, read ["$dynamicAnchor"]: string?,
    read ["$defs"]: { read [string]: JSONSchema }?, read title: string?, read description: string?,
    read deprecated: boolean?, read readOnly: boolean?, read writeOnly: boolean?,
}
export type ValueOnlyJSONSchema = { read enum: { read [number]: JSONSchemaValue }?, read const: JSONSchemaValue? }
export type NullJSONSchema = BaseJSONSchema & {
    read type: "null", read enum: { read [number]: JsonNull }?, read const: JsonNull?, read default: JsonNull?, read examples: { read [number]: JsonNull }?,
}
export type BooleanJSONSchema = BaseJSONSchema & {
    read type: "boolean", read enum: { read [number]: boolean }?, read const: boolean?, read default: boolean?, read examples: { read [number]: boolean }?,
}
export type NumericJSONSchema = BaseJSONSchema & {
    read type: "number" | "integer", read enum: { read [number]: number }?, read const: number?, read default: number?, read examples: { read [number]: number }?,
    read multipleOf: number?, read maximum: number?, read exclusiveMaximum: number?, read minimum: number?, read exclusiveMinimum: number?,
}
export type TextJSONSchema<F = JSONSchemaFormat> = BaseJSONSchema & {
    read type: "string", read enum: { read [number]: string }?, read const: string?, read default: string?, read examples: { read [number]: string }?,
    read format: F?, read maxLength: number?, read minLength: number?, read pattern: string?, read contentEncoding: string?,
    read contentMediaType: string?, read contentSchema: JSONSchema?,
}
export type ArrayJSONSchema = BaseJSONSchema & {
    read type: "array", read enum: { read [number]: JsonArray }?, read const: JsonArray?, read default: JsonArray?, read examples: { read [number]: JsonArray }?,
    read items: JSONSchema?, read contains: JSONSchema?, read prefixItems: { read [number]: JSONSchema }?, read maxItems: number?,
    read minItems: number?, read uniqueItems: boolean?, read maxContains: number?, read minContains: number?, read unevaluatedItems: JSONSchema?,
}
export type ObjectJSONSchema = BaseJSONSchema & {
    read type: "object", read enum: { read [number]: JsonObject }?, read const: JsonObject?, read default: JsonObject?, read examples: { read [number]: JsonObject }?,
    read properties: { read [string]: JSONSchema }?, read additionalProperties: JSONSchema?, read patternProperties: { read [string]: JSONSchema }?,
    read propertyNames: JSONSchema?, read maxProperties: number?, read minProperties: number?, read required: { read [number]: string }?,
    read dependentRequired: { read [string]: { read [number]: string } }?, read unevaluatedProperties: JSONSchema?,
}
-- Luau has no conditional types or nonempty tuple types. The unrestricted
-- keyword model represents nested/composed schemas without an impossible intersection.
export type NestedJSONSchema = SchemaKeywords
export type ComposedJSONSchema = SchemaKeywords
export type TypedJSONSchema = SchemaKeywords
export type ExpressiveTextJSONSchema<F = JSONSchemaFormat> = BaseJSONSchema & {
    read type: "string", read enum: { read [number]: string }?, read const: string?, read default: string?, read examples: { read [number]: string }?,
    read format: F?, read maxLength: number?, read minLength: number?, read pattern: string?, read contentEncoding: string?,
    read contentMediaType: string?, read contentSchema: ExpressiveJSONSchema?,
}
export type ExpressiveArrayJSONSchema = BaseJSONSchema & {
    read type: "array", read enum: { read [number]: JsonArray }?, read const: JsonArray?, read default: JsonArray?, read examples: { read [number]: JsonArray }?,
    read items: ExpressiveJSONSchema?, read contains: ExpressiveJSONSchema?, read prefixItems: { read [number]: ExpressiveJSONSchema }?, read maxItems: number?,
    read minItems: number?, read uniqueItems: boolean?, read maxContains: number?, read minContains: number?, read unevaluatedItems: ExpressiveJSONSchema?,
}
export type ExpressiveObjectJSONSchema = BaseJSONSchema & {
    read type: "object", read enum: { read [number]: JsonObject }?, read const: JsonObject?, read default: JsonObject?, read examples: { read [number]: JsonObject }?,
    read properties: { read [string]: ExpressiveJSONSchema }?, read additionalProperties: (ExpressiveJSONSchema | boolean)?, read patternProperties: { read [string]: ExpressiveJSONSchema }?,
    read propertyNames: ExpressiveTextJSONSchema?, read maxProperties: number?, read minProperties: number?, read required: { read [number]: string }?,
    read dependentRequired: { read [string]: { read [number]: string } }?, read unevaluatedProperties: ExpressiveJSONSchema?,
}
export type ExpressiveJSONSchema = NullJSONSchema | BooleanJSONSchema | NumericJSONSchema
    | ExpressiveTextJSONSchema | ExpressiveArrayJSONSchema | ExpressiveObjectJSONSchema
    | (BaseJSONSchema & { read anyOf: { read [number]: ExpressiveJSONSchema } })
    | (BaseJSONSchema & { read oneOf: { read [number]: ExpressiveJSONSchema } })
    | (BaseJSONSchema & { read ["$ref"]: string })

return table.freeze({})
