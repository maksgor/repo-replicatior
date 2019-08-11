from aiohttp.web import HTTPFound, Response

from repo_replicator.client import (
    get_auth_url,
    get_access_token,
    copy_repository,
)


async def index(request):
    raise HTTPFound(get_auth_url(request.app['config']['client_id']))


async def callback(request):
    code = request.query.get('code')

    if not code:
        return Response(text='Code not provided')

    access_token = await get_access_token(
        request.app['client_session'],
        code,
        request.app['config']['client_id'],
        request.app['config']['client_secret'],
    )

    if not access_token:
        return Response(text='No access token')

    new_repo_data = await copy_repository(
        request.app['client_session'],
        access_token,
        request.app['config']['repo'],
    )

    if new_repo_data.get('errors'):
        return Response(
            text='\n'.join(err for err in new_repo_data['errors'])
        )

    if not new_repo_data.get('html_url'):
        return Response(
            text='Something went wrong'
        )

    raise HTTPFound(new_repo_data.get('html_url'))
