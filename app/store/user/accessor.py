import datetime

from sqlalchemy import select, update, delete, join, ScalarResult

from app.user.models import User, UserModel, ReferralCode, ReferralCodeModel, ReferralModel, Referral
from app.base.base_accessor import BaseAccessor


class UserAccessor(BaseAccessor):
    async def get_user_by_email(self, email: str) -> User | None:
        query = select(UserModel).where(UserModel.email == email)

        async with self.app.database.session() as session:
            user: UserModel | None = await session.scalar(query)

        if not user:
            return None

        return User(id=user.id, email=user.email, password=user.password, referral_code_id=user.referral_code_id)

    async def create_user(self, email: str, password: str) -> User:
        new_user = UserModel(email=email, password=User.hash_password(password))

        async with self.app.database.session() as session:
            session.add(new_user)
            await session.commit()

        return User(id=new_user.id, email=new_user.email, password=new_user.password)

    async def create_token(self, token: str, created_at: datetime.datetime, user_id: int,) -> ReferralCode:
        new_referral_code = ReferralCodeModel(token=token, created_at=created_at, expiration_date=(created_at + datetime.timedelta(days=7)), user_id=user_id)
        query = update(UserModel).where(UserModel.id == user_id).values(referral_code_id=new_referral_code.id)

        async with self.app.database.session() as session:
            session.add(new_referral_code)
            await session.commit()

            await session.execute(query)
            await session.commit()

        return ReferralCode(id=new_referral_code.id, token=new_referral_code.token, created_at=new_referral_code.created_at, expiration_date=new_referral_code.expiration_date, user_id=new_referral_code.user_id)

    async def delete_referral_code(self, referral_code_id: int) -> None:
        async with self.app.database.session() as session:

            await session.execute(delete(ReferralCodeModel).where(ReferralCodeModel.id == referral_code_id))
            await session.commit()

    async def get_referral_code_by_email(self, email: str) -> ReferralCode | None:
        user_id_subquery = select(UserModel.id).where(UserModel.email == email).scalar_subquery()
        query = select(ReferralCodeModel).join(UserModel, ReferralCodeModel.user_id == UserModel.id).where(ReferralCodeModel.user_id == user_id_subquery)

        async with self.app.database.session() as session:
            referral_code: ReferralCodeModel | None = await session.scalar(query)

        if not referral_code:
            return None

        return ReferralCode(id=referral_code.id, token=referral_code.token, created_at=referral_code.created_at, expiration_date=referral_code.expiration_date, user_id=referral_code.user_id)

    async def get_referral_code(self, referral_code: str) -> str | None:
        query = select(ReferralCodeModel).where(ReferralCodeModel.token == referral_code)

        async with self.app.database.session() as session:
            referral_code: str | None = await session.scalar(query)

        if not referral_code:
            return None

        return referral_code

    async def get_referral_by_email(self, email: str) -> Referral | None:
        query = select(ReferralModel).where(ReferralModel.email == email)

        async with self.app.database.session() as session:
            referral: ReferralModel | None = await session.scalar(query)

        if not referral:
            return None

        return Referral(id=referral.id, email=referral.email, password=referral.password)

    async def create_referral(self, email: str, password: str, ref_code_id: int, ref_id) -> Referral:
        new_referral = ReferralModel(email=email, password=User.hash_password(password), referral_code_id=ref_code_id, referrer_id=ref_id)

        async with self.app.database.session() as session:
            session.add(new_referral)
            await session.commit()

        return Referral(id=new_referral.id, email=new_referral.email, password=new_referral.password, referral_code_id=new_referral.referral_code_id, referrer_id=new_referral.referrer_id)

    async def list_referrals(self, referrals_id: int) -> list[Referral]:
        if referrals_id:
            query = select(ReferralModel).select_from(join(ReferralModel, UserModel, ReferralModel.referrer_id == UserModel.id)).where(UserModel.id == int(referrals_id))

            async with self.app.database.session() as session:
                referrals: ScalarResult[ReferralModel] = await session.execute(query)

            return [Referral(id=row[0].id, email=row[0].email, password=row[0].password, referral_code_id=row[0].referral_code_id, referrer_id=row[0].referrer_id) for row in referrals]
