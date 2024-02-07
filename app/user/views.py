import datetime

from aiohttp.web import HTTPForbidden
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp_apispec import request_schema, response_schema, docs, querystring_schema
from aiohttp_session import new_session
import jwt

from app.user.schemes import UserSchema, ReferralCodeSchema, ReferralSchema, UserIdSchema, ListReferralSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class UserRegisterView(View):
    @docs(tags=["API-server"], summary="Register for user as referrer")
    @request_schema(UserSchema)
    @response_schema(UserSchema, 200)
    async def post(self):
        data = await self.request.json()
        try:
            email = data["email"]
            password = data["password"]
        except KeyError:
            raise HTTPBadRequest(reason="Invalid request body. Missing required fields")

        user = await self.store.users.get_user_by_email(email)
        if user:
            raise HTTPForbidden(reason="User with provided email already exist")

        new_user = await self.store.users.create_user(email, password)
        raw_user = UserSchema().dump(new_user)
        session = await new_session(request=self.request)
        session["user"] = raw_user
        return json_response(data=raw_user)


class UserLoginView(View):
    @docs(tags=["API-server"], summary="Login for user as referrer")
    @request_schema(UserSchema)
    @response_schema(UserSchema, 200)
    async def post(self):
        data = await self.request.json()
        try:
            email = data["email"]
            password = data["password"]
        except KeyError:
            raise HTTPBadRequest(reason="Invalid request body. Missing required fields")

        user = await self.store.users.get_user_by_email(email)
        if not user:
            raise HTTPForbidden(reason="No user with provided email was found")

        if not user.is_password_valid(password):
            raise HTTPForbidden(reason="Invalid credentials")

        raw_user = UserSchema().dump(user)
        session = await new_session(request=self.request)
        session["user"] = raw_user
        return json_response(data=raw_user)


class CreateReferralCodeView(AuthRequiredMixin, View):
    @docs(tags=["API-server"], summary="Add new referral code for user", description="Add new referral code to database")
    @response_schema(ReferralSchema, 200)
    async def post(self):
        if self.request.user.referral_code_id:
            return HTTPBadRequest(reason="User already has a referral code")

        token = jwt.encode({"email": self.request.user.email}, self.request.app.get_secret_key(), algorithm="HS256")
        referral_code = await self.store.users.create_token(token=token, user_id=self.request.user.id,
                                                           created_at=datetime.datetime.utcnow())

        self.request.user.referral_code_id = referral_code.id

        raw_referral_code = ReferralCodeSchema().dump(referral_code)
        return json_response(data=raw_referral_code)


class DeleteReferralCodeView(AuthRequiredMixin, View):
    @docs(tags=["API-server"], summary="Delete referral code from user", description="Delete referral code from database")
    @response_schema(UserSchema, 200)
    async def post(self):
        if not self.request.user.referral_code_id:
            return HTTPBadRequest(reason="User doesn't have a referral code")

        self.request.user.referral_code_id = await self.store.users.delete_referral_code(self.request.user.referral_code_id)
        raw_user = UserSchema().dump(self.request.user)
        return json_response(data=raw_user)


class GetReferralCodeByEmailView(AuthRequiredMixin, View):
    @docs(tags=["API-server"], summary="Get referral code by user's email")
    @request_schema(UserSchema)
    @response_schema(ReferralCodeSchema, 200)
    async def get(self):
        data = await self.request.json()
        try:
            email = data["email"]
        except KeyError:
            raise HTTPBadRequest(reason="Invalid request body. Missing required fields")

        user = await self.store.users.get_user_by_email(email)
        if not user:
            raise HTTPForbidden(reason="No user with provided email was found")

        referral_code = await self.store.users.get_referral_code_by_email(email)
        if not referral_code:
            raise HTTPForbidden(reason="The user doesn't have a referral code")
        raw_referral_code = ReferralCodeSchema().dump(referral_code)
        return json_response(data=raw_referral_code)


class ReferralListView(AuthRequiredMixin, View):
    @docs(tags=["API-server"], summary="List referral codes", description="List referral codes from database")
    @request_schema(UserIdSchema)
    @response_schema(ListReferralSchema)
    async def get(self):
        try:
            referrer_id = self.request.query.get("referrer_id")
        except KeyError:
            referrer_id = None

        referrals = await self.store.users.list_referrals(referrer_id)
        if not referrals:
            raise HTTPForbidden(reason="The referrer with this id has no referrals")
        raw_referrals = [ReferralSchema().dump(referral) for referral in referrals]
        return json_response(data={"referrals": raw_referrals})


class ReferralRegisterView(View):
    @docs(tags=["API-server"], summary="Register for user as referral")
    @request_schema(ReferralSchema)
    @response_schema(ReferralSchema, 200)
    async def post(self):
        data = await self.request.json()
        try:
            email = data["email"]
            password = data["password"]
            referral_code = data["referral_code"]
        except KeyError:
            raise HTTPBadRequest(reason="Invalid request body. Missing required fields")

        ref_code = await self.store.users.get_referral_code(referral_code)

        if not ref_code:
            raise HTTPForbidden(reason="This referral code doesn't exist")

        referral = await self.store.users.get_referral_by_email(email)
        if referral:
            raise HTTPForbidden(reason="Referral with provided email already exist")

        new_referral = await self.store.users.create_referral(email, password, ref_code.id, ref_code.user_id)
        raw_referral = ReferralSchema().dump(new_referral)
        session = await new_session(request=self.request)
        session["referral"] = raw_referral
        print(session)
        return json_response(data=raw_referral)

