import datetime

from aiohttp.web import HTTPForbidden
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import new_session
import jwt

from app.user.schemes import UserSchema, AccessTokenSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class UserRegisterView(View):
    @docs(tags=["user"], summary="Login for user")
    @request_schema(UserSchema)
    @response_schema(UserSchema, 200)
    async def post(self):
        data = await self.request.json()
        try:
            email = data["email"]
            password = data["password"]
        except KeyError:
            raise HTTPBadRequest(reason="Invalid request body. Missing required fields")

        user = await self.store.users.get_by_email(email)
        if user:
            raise HTTPForbidden(reason="User with provided email already exist")

        new_user = await self.store.users.create_user(email, password)
        raw_user = UserSchema().dump(new_user)
        return json_response(data=raw_user)


class UserLoginView(View):
    @docs(tags=["user"], summary="Login for user")
    @request_schema(UserSchema)
    @response_schema(UserSchema, 200)
    async def post(self):
        data = await self.request.json()
        try:
            email = data["email"]
            password = data["password"]
        except KeyError:
            raise HTTPBadRequest(reason="Invalid request body. Missing required fields")

        user = await self.store.users.get_by_email(email)
        if not user:
            raise HTTPForbidden(reason="No user with provided email was found")

        if not user.is_password_valid(password):
            raise HTTPForbidden(reason="Invalid credentials")

        raw_user = UserSchema().dump(user)
        session = await new_session(request=self.request)
        session["user"] = raw_user
        return json_response(data=raw_user)


class CreateRefCode(AuthRequiredMixin, View):
    async def post(self):
        print(self.request.user.email)
        if self.request.user.referral_code:
            return HTTPBadRequest(reason="User already has a referral code")

        token = jwt.encode({"email": self.request.user.email}, self.request.app.get_secret_key(), algorithm="HS256")
        access_token = await self.store.users.create_token(token=token, user_id=self.request.user.id,
                                                           created_at=datetime.datetime.utcnow())

        self.request.user.referral_code = access_token

        raw_user = UserSchema().dump(self.request.user)
        return json_response(data=raw_user)


class DeleteRefCodeView(AuthRequiredMixin, View):
    async def post(self):
        await self.store.users.delete_referral_code(self.request.user.email)
        raw_user = UserSchema().dump(self.request.user)
        return json_response(data=raw_user)


class GetRefCodeByEmail(AuthRequiredMixin, View):
    @response_schema(AccessTokenSchema, 200)
    async def get(self):
        ref_code = await self.store.users.get_ref_code_by_email(self.request.user.email)
        raw_ref_code = AccessTokenSchema().dump(ref_code)
        return json_response(data=raw_ref_code)
