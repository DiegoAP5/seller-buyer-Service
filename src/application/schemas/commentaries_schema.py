from marshmallow import Schema, fields

class CommentariesSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    comments = fields.Str(required=True)
    sellerId = fields.Int(required=True)
