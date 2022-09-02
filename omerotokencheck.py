#!/usr/bin/env python

import sys
import requests

# To implement, subclass
# https://github.com/ome/omero-server/blob/v5.6.1/src/main/java/ome/security/auth/FilePasswordProvider.java
# https://docs.openmicroscopy.org/omero-server/5.5.0/javadoc/index.html?ome/security/SecurityFilter.html
# 
# Configuration omero.security.password_provider
#
# Let's call it the new password provider GlobusTokenValidator
#
# In GlobusTokenValidator add a couple of Fields (Properties?)
# or configuration options
# client_id
# client_secret
# introspection_url
# identity_provider

# omero.security.password_provider=GlobusTokenValidator
# not sure how to set the fields on the password_provider

# Look examples of RFC 7662 OAuth token introspection, like
# https://connect2id.com/products/nimbus-oauth-openid-connect-sdk/examples/oauth/token-introspection

# https://docs.globus.org/api/auth/developer-guide/#register-app

# OMERO Server Globus Auth App
SERVICE_CLIENT_ID = '532e2b47-3a52-4f17-966c-05634c57468a'
SERVICE_CLIENT_SECRET = '<put secret here>'
SCOPE = 'https://auth.globus.org/scopes/532e2b47-3a52-4f17-966c-05634c57468a/omero'

# https://docs.globus.org/api/auth/reference/#token-introspect
INTROSPECTION_URL = 'https://auth.globus.org/v2/oauth2/token/introspect'

# Required identity provider domain to get the username from
# This app requires users to have a UCSD identity and authenticate with it
IDENTITY_PROVIDER = 'ucsd.edu'

# Simulate the list of accepted usernames
PROPERTIES = ['rpwagner', 'wcwest', 'bay001']

def doCheckPassword(omero_username, token):
    # Calls the Globus RFC 7662 OAuth 2.0 Token Introspection URL
    # Returns True if
    #  - the omero_username is in the list of allowed users
    #  - the token is active
    #  - the token scope is for this server
    #  - the user is from UCSD
    #  - the omero_username trying to login matches the email of the
    #    user granted the token
    # Otherwise, returns False

    # user needs to be in "database" of allowed users
    if omero_username not in PROPERTIES:
        return False
    resp = requests.post(
        INTROSPECTION_URL,
        data={'token': token, 'include': 'identity_set_detail'},
        auth=(SERVICE_CLIENT_ID, SERVICE_CLIENT_SECRET),
        verify=True)
    resp_dict = resp.json()
    # Make sure this is a valid token for this server
    if not resp_dict['active'] or SCOPE != resp_dict['scope']:
        return False
    # Check the domain of the username and that the
    # email username matches the user trying to log in
    username, domain = resp_dict['username'].split('@', 1)
    email, email_domain = resp_dict['email'].split('@', 1)
    if domain == IDENTITY_PROVIDER and email == omero_username:
        return True
    return False

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: omerotokencheck.py <username> <access token>')
        sys.exit(1)
    exit_code = 0
    try:
        tf = doCheckPassword(sys.argv[1], sys.argv[2])
        if tf:
            print('valid user')
        else:
            print('invalid user')
            exit_code = 1
    except:
        print('an uknown error occurred')
        exit_code = 1
    sys.exit(exit_code)
