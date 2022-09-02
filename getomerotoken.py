#!/usr/bin/env python

import os
from globus_sdk import NativeAppAuthClient
from globus_sdk.tokenstorage import SimpleJSONFileAdapter

# The client ID doesn't matter much, so long as it's valid
# But, it's best if this client requires a UCSD
# identity.
CLIENT_ID = 'd719c82f-3a11-4de1-9d87-d52d28ec31b6'

# Be careful with enabling refresh tokens, they can leave a long-lived
# mechanism to retrieve access on your system
REFRESH_TOKENS = False

OMERO_SCOPE = 'https://auth.globus.org/scopes/532e2b47-3a52-4f17-966c-05634c57468a/omero'
OMERO_RESOURCE_SERVER = '532e2b47-3a52-4f17-966c-05634c57468a'
OMERO_TOKEN_FILE = os.path.expanduser("~/.omero-tokens.json")

if __name__ == '__main__':
    native_auth_client = NativeAppAuthClient(CLIENT_ID)
    file_adapter = SimpleJSONFileAdapter(OMERO_TOKEN_FILE)

    if not file_adapter.file_exists():
        # do a login flow, getting back initial tokens
        native_auth_client.oauth2_start_flow(
            requested_scopes=OMERO_SCOPE,
            refresh_tokens=REFRESH_TOKENS,
        )
        authorize_url = native_auth_client.oauth2_get_authorize_url()
        print(f"Please go to this URL and login:\n\n{authorize_url}\n")
        auth_code = input("Please enter the code here: ").strip()
        response = native_auth_client.oauth2_exchange_code_for_tokens(auth_code)
        # now store the tokens and pull out the Groups tokens
        file_adapter.store(response)
        tokens = response.by_scopes[OMERO_SCOPE]
    else:
        # otherwise, we already did login; load the tokens from that file
        tokens = file_adapter.get_token_data(OMERO_RESOURCE_SERVER)

    print(tokens['access_token'])
