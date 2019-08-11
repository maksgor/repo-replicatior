# REPO REPLICATOR

Self replicating repository.

## Technology stack
- python3.6+
- aiohttp
- Docker&docker-compose

## Setup

### Requirements
- Docker
- docker-compose

To run app, you have first to create own [OAuth app](https://github.com/settings/developers).

Set homepage URL field to `http://localhost:5000/` and Authorization callback URL to 
`http://localhost:5000/callback`.

Then, after you created the app, you should take `client id` and `client secret`
 on the app page and put those values to appropriate fields in `secrets/secrets.yaml`.
Also you have to add repository identifier to `repo` field which should look like
`maksgor/repo_replicator`.

### Run application
```bash
docker-compose up
```
By default, the app will be available [here](http://localhost:5000).

## How it works

When the app is running, the user enters its home page, where he is redirected to
OAuth page of Github for authorization. Access to public repos is the only, which is
requested. 

After successful authorization via Github, user is redirected by Github to
`/callback` page, where we get the one-time password to receive permanent access_token to
work with user`s public repos.

With the access token, the application goes to github api endpoint, which allows
to create repository from a template repository (in our case, the template repository
is the current one).

This application can replicate any other repository you specify, if only this repository
is template (there is a flag under the repository name field on the Settings page).
