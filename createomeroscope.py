#!/usr/bin/env python

import sys
import requests
import json

# This is a dirty hack-and-run script, as in you hack it and run it.
# You can do this each time you want to add a client scope or FQDN.
#
# Steps
# 1) register a Globus non-Native App, get a client ID and secret
#
# 2) Optional: if you want to have scopes based on the hostname,
#    add a DNS TXT record with client ID
#    see https://docs.globus.org/api/auth/reference/#add_fqdn
#
# 3) Fill in the client ID and secret in this script
#
# 4) To register an FQDN, fill in SERVICE_CLIENT_FQDN
#
# 5) To create a scope, fill in SCOPE_NAME, SCOPE_DESCRIPTION, SCOPE_SUFFIX
#
# The script will query the Globus Auth info about the client at the end

GLOBUS_AUTH_BASE_URL = 'https://auth.globus.org/v2'

# https://docs.globus.org/api/auth/developer-guide/#register-app
SERVICE_CLIENT_ID = '532e2b47-3a52-4f17-966c-05634c57468a'
SERVICE_CLIENT_SECRET = '<put secret here>'

# https://docs.globus.org/api/auth/reference/#add_fqdn
SERVICE_CLIENT_FQDN = 'hub.stratus.jupyter-security.info'

# https://docs.globus.org/api/auth/reference/#create_scope
SCOPE_NAME = 'OMERO Server' # a short name for the scope
SCOPE_DESCRIPTION = 'OMERO Server Token Introspection' # longer text
SCOPE_SUFFIX = 'omero' # short string

if not SERVICE_CLIENT_ID or not SERVICE_CLIENT_SECRET:
    print('need SERVICE_CLIENT_ID and SERVICE_CLIENT_SECRET')
    sys.exit(1)

if SERVICE_CLIENT_FQDN:
    print('registering client FQDN: {}'.format(SERVICE_CLIENT_FQDN))
    fqdns_url = '{}/api/clients/{}/fqdns'.format(GLOBUS_AUTH_BASE_URL,
                                                     SERVICE_CLIENT_ID)
    fqdn_payload = {'fqdn': SERVICE_CLIENT_FQDN}
    resp = requests.post(fqdns_url, data=fqdn_payload,
                             auth=(SERVICE_CLIENT_ID, SERVICE_CLIENT_SECRET),
                             verify=True)
    print('FQDN response code and text')
    print(resp.status_code)
    json_object = json.loads(resp.text)
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)

else:
    print('not registering an FQDN in this pass')

if SCOPE_NAME and SCOPE_DESCRIPTION and SCOPE_SUFFIX:
    print('creating {} scope: "{}"'.format(SCOPE_SUFFIX, SCOPE_NAME))
    scopes_url = '{}/api/clients/{}/scopes'.format(GLOBUS_AUTH_BASE_URL,
                                                    SERVICE_CLIENT_ID)
    scope_payload = {'scope':
                        {
                            'name': SCOPE_NAME,
                            'description': SCOPE_DESCRIPTION,
                            'scope_suffix': SCOPE_SUFFIX
                    }
            }
    resp = requests.post(scopes_url, data=scope_payload,
                             auth=(SERVICE_CLIENT_ID, SERVICE_CLIENT_SECRET),
                             verify=True)

    print('scope response code and text')
    print(resp.status_code)
    json_object = json.loads(resp.text)
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)

else:
    print('not creating a scope in this pass')

print('getting client info')
client_url = '{}/api/clients/{}'.format(GLOBUS_AUTH_BASE_URL,
                                            SERVICE_CLIENT_ID)
resp = requests.get(client_url,
                        auth=(SERVICE_CLIENT_ID, SERVICE_CLIENT_SECRET),
                        verify=True)
print('Globus Auth client info')
print(resp.status_code)
json_object = json.loads(resp.text)
json_formatted_str = json.dumps(json_object, indent=2)
print(json_formatted_str)
