from marshmallow import Schema, fields


class EventSchema(Schema):
    uid = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
    date = fields.Date()
    time = fields.Time()
    type = fields.String()
    address = fields.String()
    seats = fields.Integer()


event_schema = EventSchema(many=True)


class LocationSchema(Schema):
    uid = fields.Integer(dump_only=True)
    title = fields.String()
    code = fields.String()


location_schema = LocationSchema(many=True)
