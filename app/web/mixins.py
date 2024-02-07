from aiohttp.abc import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden
from aiohttp_session import get_session

from app.user.models import User


class AuthRequiredMixin:
    async def _iter(self) -> StreamResponse:
        session = await get_session(self.request)
        if session.new:
            raise HTTPUnauthorized(reason="the user is not authorized")
        user_data: dict = session.get("user")
        if not user_data:
            raise HTTPForbidden
        user_email = user_data.get("email")
        if not user_email:
            raise HTTPForbidden
        user = await self.store.users.get_user_by_email(user_email)
        if not user:
            raise HTTPForbidden
        self.request.user = user
        return await super()._iter()