from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(required=False)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    referral_code = fields.Str(required=False)


class AccessTokenSchema(Schema):
    id = fields.Int(required=True)
    token = fields.Str(required=True)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    expiration_date = fields.DateTime(required=True)
