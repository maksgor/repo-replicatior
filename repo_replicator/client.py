import random
import string

BASE_AUTH_URL = 'https://github.com/login/oauth'
BASE_API_URL = 'https://api.github.com'
AUTH_SCOPE = 'public_repo'


def generate_string(length=4):
    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length)
    )


def get_auth_url(client_id):
    return f'{BASE_AUTH_URL}/authorize?' \
           f'client_id={client_id}' \
           f'&scope={AUTH_SCOPE}&state={generate_string()}'


async def get_access_token(session, code, client_id, client_secret):
    response = await session.post(
        f'{BASE_AUTH_URL}/access_token',
        headers={
            'Accept': 'application/json',
        },
        json={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
        }
    )

    response = await response.json()

    return response.get('access_token')


async def copy_repository(session, access_token, repo):
    response = await session.post(
        f'{BASE_API_URL}/repos/{repo}/generate',
        headers={
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.baptiste-preview+json',
        },
        json={
            'name': f'repo_replicator-{generate_string()}'
        }
    )

    response = await response.json()

    return response
