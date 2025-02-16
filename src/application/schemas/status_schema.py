from marshmallow import Schema, fields

class StatusSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
