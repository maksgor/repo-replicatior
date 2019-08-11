import os
import sys
import logging

from aiohttp import web, ClientSession

from repo_replicator.views import index, callback

logger = logging.getLogger(__name__)


def parse_config_from_env():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    repo = os.getenv('REPO')
    port = os.getenv('PORT', 5000)

    if not all([client_id, client_secret, repo]):
        logger.error('Values not provided')
        sys.exit(1)

    return {
        'client_id': client_id,
        'client_secret': client_secret,
        'repo': repo,
        'port': port,
    }


async def init_session(app):
    app['client_session'] = ClientSession()


async def close_session(app):
    if app['client_session']:
        await app['client_session'].close()


def run_app():
    app = web.Application()

    app['config'] = parse_config_from_env()

    app.router.add_get('/', index)
    app.router.add_get('/callback', callback)

    app.on_startup.append(init_session)
    app.on_cleanup.append(close_session)

    web.run_app(
        app,
        host='0.0.0.0',
        port=app['config']['port'],
    )
