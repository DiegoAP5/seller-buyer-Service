from marshmallow import Schema, fields

class DeliverySchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    date = fields.Date(required=True)
    clothId = fields.Int(required=True)
    location = fields.Str(required=True)
    buyer = fields.Str(required=True)
    cellphone = fields.Str(required=True)
    comments = fields.Str(required=True)
    statusId = fields.Int(required=True)
    sellerId = fields.Int(required=True)
    buyerId = fields.Int(required=True)
    offerId = fields.Int(required=True)
