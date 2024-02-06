from aiohttp.web_app import Application


def setup_routes(app: Application):
    from app.user.routes import setup_routes as user_setup_routes

    user_setup_routes(app)
