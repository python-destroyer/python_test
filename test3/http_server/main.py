from aiohttp import web

from settings import config
from routes import setup_routes

app = web.Application()
setup_routes(app)
web.run_app(app,host=config['host'], port=config['port'])