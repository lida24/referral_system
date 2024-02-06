import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.user.views import UserRegisterView, UserLoginView, CreateRefCode, DeleteRefCodeView, GetRefCodeByEmail

    app.router.add_view("/user.register", UserRegisterView)
    app.router.add_view("/user.login", UserLoginView)
    app.router.add_view("/user.create_ref_code", CreateRefCode)
    app.router.add_view("/user.delete_ref_code", DeleteRefCodeView)
    app.router.add_view("/user.get_ref_code", GetRefCodeByEmail)