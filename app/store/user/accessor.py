import datetime

from sqlalchemy import select, update, delete

from app.user.models import User, UserModel, AccessToken, AccessTokenModel
from app.base.base_accessor import BaseAccessor


class UserAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> User | None:
        query = select(UserModel).where(UserModel.email == email)

        async with self.app.database.session() as session:
            user: UserModel | None = await session.scalar(query)

        if not user:
            return None

        return User(id=user.id, email=user.email, password=user.password)

    async def create_user(self, email: str, password: str) -> User:
        new_user = UserModel(id=1, email=email, password=User.hash_password(password))

        async with self.app.database.session() as session:
            session.add(new_user)
            await session.commit()

        return User(id=new_user.id, email=new_user.email, password=new_user.password)

    async def get_by_referral_code(self, referral_code: str) -> User | None:
        query = select(UserModel).filter_by(UserModel.referral_code == referral_code).first()

        async with self.app.database.session.begin() as session:
            user: UserModel | None = await session.scalar(query)

        if not user:
            return None

        return User(id=user.id, email=user.email, referral_code=user.referral_code, referral_expiration=user.referral_expiration, password=user.password)

    async def create_token(self, token: str, user_id: int, created_at: datetime.datetime) -> AccessToken:
        new_token = AccessTokenModel(id=1, token=token, user_id=user_id, created_at=created_at, expiration_date = created_at + datetime.timedelta(days=7))
        query = update(UserModel).where(UserModel.id == user_id).values(referral_code=new_token.token)

        async with self.app.database.session() as session:
            session.add(new_token)
            await session.commit()

            await session.execute(query)
            await session.commit()

        return AccessToken(id=new_token.id, token=new_token.token, user_id=new_token.user_id, created_at=new_token.created_at, expiration_date=new_token.expiration_date)

    async def delete_referral_code(self, email: str) -> None:
        query = select(UserModel).where(UserModel.email == email)

        async with self.app.database.session() as session:
            user: UserModel = await session.scalar(query)
            await session.execute(delete(AccessTokenModel).where(AccessTokenModel.token == user.referral_code))
            await session.commit()

            user.referral_code = None
            await session.commit()

    async def get_ref_code_by_email(self, email: str) -> AccessToken:
        query = select(UserModel).where(UserModel.email == email)

        async with self.app.database.session() as session:
            user: UserModel = await session.scalar(query)
            access_token: AccessTokenModel = await session.scalar(select(AccessTokenModel).where(AccessTokenModel.user_id == user.id))

        return AccessToken(id=access_token.id, token=access_token.token, user_id=access_token.user_id,
                           created_at=access_token.created_at, expiration_date=access_token.expiration_date)