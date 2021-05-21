# Securing JupyterHub

Four steps:

1. HTTPS at Boundary
1. Configure Internal SSL
1. Set IPC Kernel Communications
1. Configure External Authenticator

## Documentation

Existing guidelines
Look at reference google doc

Slides
https://docs.google.com/presentation/d/178agvhzTrA14dP0GrN9Aa37EZIzc0kFb7fDbF_wpnPg/edit#slide=id.g64fed3c726_1_511

## Setup & Architecture

## Unencrypted Channels

## HTTPS at Boundary

## Configure Internal SSL

## Set IPC Kernel Communications

## Configure External Authenticator

```
from oauthenticator.globus import LocalGlobusOAuthenticator
c.JupyterHub.authenticator_class = LocalGlobusOAuthenticator
c.LocalGlobusOAuthenticator.enable_auth_state = True
c.LocalGlobusOAuthenticator.oauth_callback_url = \
     'https://trusted-ci<N>.globus-training.net/jhub/hub/oauth_callback'
c.LocalGlobusOAuthenticator.client_id = '<>'
c.LocalGlobusOAuthenticator.client_secret = '<>'
c.LocalGlobusOAuthenticator.create_system_users = True
```
