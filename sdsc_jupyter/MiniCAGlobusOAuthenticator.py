import os
import subprocess
from traitlets import Unicode
from oauthenticator.globus import LocalGlobusOAuthenticator

# To Do
# Check "real" retrieval of user CA
# Spawner: it should be able to pull the auth state
# How to execute batch command over SSH? I.e., how to pass user CA?

class MiniCAGlobusOAuthenticator(LocalGlobusOAuthenticator):
    mini_ca_scope = Unicode(
        help="""Scope for the token sent to the Mini CA.""").tag(config=True)

    def _mini_ca_scope_default(self):
        return os.getenv('MINI_CA_SCOPE', '')

    mini_ca_host = Unicode(
        help="""Host to send the Mini CA SSH request.""").tag(config=True)

    def _mini_ca_host_default(self):
        return os.getenv('MINI_CA_HOST', '')

    mini_ca_cmd = Unicode(
        help="""Mini CA command to use.""").tag(config=True)

    def _mini_ca_cmd_default(self):
        return os.getenv('MINI_CA_CMD', '/home/ubuntu/minicatokencheck.py')
    
    async def authenticate(self, handler, data=None):
        if not self.mini_ca_scope in self.scope:
            self.scope.append(self.mini_ca_scope)
        user_info = await super().authenticate(handler, data=data)
        # strip off mini CA token, save for reuse
        old_tokens = user_info['auth_state']['tokens']
        new_tokens = {}
        mini_ca_token = None
        for resource_server in old_tokens.keys():
            if old_tokens[resource_server]['scope'] == self.mini_ca_scope:
                mini_ca_token = old_tokens[resource_server]['access_token']
            else:
                new_tokens[resource_server] = old_tokens[resource_server]
        user_info['auth_state']['tokens'] = new_tokens

        ssh_cmd = '{} {} {}'.format(self.mini_ca_host,
                                        self.mini_ca_cmd, mini_ca_token)
        ssh = subprocess.Popen(["ssh", ssh_cmd],
                                   shell=False,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result:
            user_info['auth_state']['mini_ca'] = result
        return user_info
