from marshmallow import Schema, fields

class CommentariesSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    clothId = fields.Int(required=True)
    offer = fields.Float(required=True)
    buyerId = fields.Int(required=True)
    sellerId = fields.Int(required=True)
