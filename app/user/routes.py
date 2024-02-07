import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.user.views import UserRegisterView, UserLoginView, CreateReferralCodeView, DeleteReferralCodeView, GetReferralCodeByEmailView, ReferralRegisterView, ReferralListView

    app.router.add_view("/user.register", UserRegisterView)
    app.router.add_view("/user.login", UserLoginView)
    app.router.add_view("/user.create_ref_code", CreateReferralCodeView)
    app.router.add_view("/user.delete_ref_code", DeleteReferralCodeView)
    app.router.add_view("/user.get_ref_code", GetReferralCodeByEmailView)
    app.router.add_view("/referral.register", ReferralRegisterView)
    app.router.add_view("/user.list_referrals", ReferralListView)
