from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(required=False)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    referral_code_id = fields.Int(required=False)


class ReferralCodeSchema(Schema):
    id = fields.Int(required=True)
    token = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    expiration_date = fields.DateTime(required=True)
    user_id = fields.Int(required=True)


class ReferralSchema(Schema):
    id = fields.Int(required=False)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    referral_code_id = fields.Int(required=False)
    referrer_id = fields.Int(required=False)


class UserIdSchema(Schema):
    referrer_id = fields.Int()


class ListReferralSchema(Schema):
    referrals = fields.Nested(ReferralSchema, many=True)